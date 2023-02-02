#!/usr/bin/env python
# * coding: utf8 *
"""
A provider that queries data in Open SGID
"""
import re

from psycopg_pool import ConnectionPool
from tenacity import retry, stop_after_attempt, wait_exponential

DATABASE = 'opensgid'
AGRC = 'agrc'
HOST = 'opensgid.agrc.utah.gov'
SPLITTER = '-'

#: geometry types
POINT = 'point'
POLYGON = 'polygon'

#: field names
XID = 'xid'
FULLADD = 'fulladd'
ADDSYSTEM = 'addsystem'
CITY = 'city'
NAME = 'name'

RETRY_WAIT_MIN = 0.5
RETRY_WAIT_MAX = 5
RETRY_ATTEMPTS = 3

#: search field types
TEXT = 'text'
NUMERIC = 'numeric'

directions = ['north', 'south', 'east', 'west']
normalize_direction_infos = []
for direction in directions:
    #: build a list of all of the different ways to type the direction
    #: e.g. (no, no., nor, nor., ...)
    permutations = []
    for index in range(len(direction)):
        permutation = direction[0:index + 1]
        permutations.append(permutation)
        permutations.append(f'{permutation}.')
    normalize_direction_infos.append((re.compile(fr'^(\d+) ({"|".join(permutations)})( |$)'), direction[0]))

pool = ConnectionPool(f'dbname={DATABASE} user={AGRC} password={AGRC} host={HOST}')


class DatabaseConnection():
    """ used to interact with the open sgid database
    """

    @retry(
        stop=stop_after_attempt(RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=0.5, min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX)
    )
    def query(self, query):
        """ get records from the database
        """
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                return cursor.fetchall()

    @retry(
        stop=stop_after_attempt(RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=0.5, min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX)
    )
    def get_magic_key_record(self, query):
        """ get record associate with magic key query

        returns a tuple with the record and a list of field names
        """
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                return (cursor.fetchone(), [desc[0] for desc in cursor.description if desc[0] != 'shape'])


database = DatabaseConnection()


class Table():
    """ object that orchestrates communication with a specific table in open sgid
    """
    SPLITTER = '-'

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        table_name,
        search_field,
        geometry_type,
        search_field_type=TEXT,
        additional_out_fields=None,
        get_suggestion_text_from_record=None,
        search_key=None
    ):
        self.table_name = table_name
        self.search_field = search_field

        if geometry_type not in [POINT, POLYGON]:
            raise ValueError(f'invalid value passed for geometry_type: {geometry_type}')
        self.geometry_type = geometry_type

        if search_field_type not in [TEXT, NUMERIC]:
            raise ValueError(f'invalid value passed for search_field_type: {search_field_type}')
        self.search_field_type = search_field_type
        self.additional_out_fields = additional_out_fields or []

        def default_get_suggestion_text(matched_text, context_values):
            if context_values and len(context_values) > 0:
                return f'{matched_text}, {", ".join(context_values)}'

            return matched_text

        self.get_suggestion_text_from_record = get_suggestion_text_from_record or default_get_suggestion_text
        self.search_key = search_key

    def get_suggestion_from_record(self, xid, matched_text, *context_values):
        """ return a suggestion dictionary based on a database record
        """

        return self.make_suggestion(xid, self.get_suggestion_text_from_record(matched_text, context_values))

    def make_suggestion(self, xid, suggestion_text):
        """ return a suggestion dictionary based on the id and match text
        """
        return {'isCollection': False, 'magicKey': f'{xid}{self.SPLITTER}{self.table_name}', 'text': suggestion_text}

    def get_suggest_query(self, search_text, limit):
        """ create a query that returns records for suggestions
        """

        #: check for match with search key e.g. '1 hou' or '1 house'
        if self.search_key is not None:
            parts = search_text.split(' ')
            if len(parts) == 2 and parts[1] in self.search_key:
                search_text = parts[0]

        if self.search_field_type == TEXT:
            where = f'{self.search_field} ilike \'{search_text}%\''
        else:  #: NUMERIC
            #: will throw ValueError if it's not a string
            int(search_text)
            where = f'{self.search_field} = {search_text}'

        return f'''
            select {self.get_out_fields()} from {self.table_name}
            where {where}
            order by {self.search_field} ASC
            limit {limit}
        '''

    def get_out_fields(self):
        """ combine all fields that we need in queries as comma-separated string
        """
        return ','.join([XID, self.search_field] + self.additional_out_fields)

    def get_suggestions(self, search_text, max_results):
        """ query for records and return them as suggestion objects
        """
        try:
            records = database.query(self.get_suggest_query(search_text, max_results))
        except ValueError:
            #: this is probably an invalid search text for a numeric field
            return []

        return [self.get_suggestion_from_record(*record) for record in records]

    def get_magic_key_query(self, xid, out_spatial_reference):
        """ create a query for getting a specific record using the xid value

        Also translates the geometry into x, y and extent fields.
        """
        if self.geometry_type == POINT:
            extent = 'st_expand(st_transform(shape, 26912), 150)'
        else:
            extent = f'st_transform(shape, {out_spatial_reference})'

        shape = f'''
            st_x(st_transform(st_centroid(shape), {out_spatial_reference})) as x,
            st_y(st_transform(st_centroid(shape), {out_spatial_reference})) as y,
            st_xmax(st_transform({extent}, {out_spatial_reference}))  as xmax,
            st_ymax(st_transform({extent}, {out_spatial_reference})) as ymax,
            st_xmin(st_transform({extent}, {out_spatial_reference})) as xmin,
            st_ymin(st_transform({extent}, {out_spatial_reference})) as ymin
        '''

        return f'''
            select {f'{self.get_out_fields()}, {shape}, *'} from {self.table_name}
            where {XID} = {xid}
        '''

    def get_candidate_from_magic_key(self, xid, out_spatial_reference):
        # pylint: disable=too-many-locals
        """ returns a candidate dictionary with the data corresponding to the value that matches the xid value
        """
        num_shape_fields = 6
        num_base_fields = len(self.additional_out_fields) + 2
        record, fieldnames = database.get_magic_key_record(self.get_magic_key_query(xid, out_spatial_reference))
        x_value, y_value, xmax, ymax, xmin, ymin = record[num_base_fields:num_base_fields + num_shape_fields]
        extra_fieldnames = fieldnames[num_base_fields + num_shape_fields:]
        extra_values = record[num_base_fields + num_shape_fields:]

        match_text = self.get_suggestion_from_record(*record[:num_base_fields])['text']
        attributes = {
            'Score': 100,  #: this shows up in the Pro locate results
            'OpenSGID Table': self.table_name,
            'Match_addr': match_text,  #: this shows up as "Description" in Pro
        }
        attributes.update(dict(zip(extra_fieldnames, extra_values)))

        return {
            'address': match_text,
            'score': 100,
            'location': {
                'x': x_value,
                'y': y_value
            },
            'attributes': attributes,
            'extent': {
                'xmax': xmax,
                'xmin': xmin,
                'ymax': ymax,
                'ymin': ymin
            },
        }


class AddressPointTable(Table):
    """ overridden to handle some specifics for address points
    """

    def get_suggestion_from_record(self, xid, matched_text, *context_values):
        """ return a suggestion dictionary based on a database record
        """
        address_system, city = context_values
        full_address = matched_text

        if city is not None:
            zone = city
        else:
            zone = address_system

        match_text = f'{full_address}, {zone}'

        return self.make_suggestion(xid, match_text)

    def get_suggest_query(self, search_text, limit):
        """ create a query that returns records for suggestions
        """

        return super().get_suggest_query(normalize_prefix_direction(search_text), limit)


def normalize_prefix_direction(search_text):
    """
    Normalize the ~first~ cardinal direction of the search text
    We don't want to mess with others that may or may not be part of the street name,
    city or some other part of the address. We could possibly push this text through usaddress
    but that seems like a perf hit that we don't want on something like a suggest endpoint
    """
    for regex, replacement in normalize_direction_infos:
        new_value = re.sub(regex, fr'\g<1> {replacement} ', search_text.lower()).rstrip()

        if new_value != search_text.lower():
            return new_value

    return new_value


class FullTextTable(Table):
    """ overridden to make a more appropriate search query
    """

    def get_suggest_query(self, search_text, limit):
        """ create a query that searches the entire field, not just the beginning
        """
        where = f'{self.search_field} ilike \'%{search_text}%\''

        return f'''
            select {self.get_out_fields()} from {self.table_name}
            where {where}
            order by {self.search_field} ASC
            limit {limit}
        '''


#: these should be ordered in the order that you want results to show up in
#: NOTE: don't forget to keep the README up-to-date with this code
TABLES = [
    Table(
        'opensgid.political.house_districts_2022_to_2032',
        'dist',
        POLYGON,
        search_field_type=NUMERIC,
        get_suggestion_text_from_record=lambda text, *rest: f'Utah House District {text}',
        search_key='utah house district',
    ),
    Table(
        'opensgid.political.school_board_districts_2022_to_2032',
        'dist',
        POLYGON,
        search_field_type=NUMERIC,
        get_suggestion_text_from_record=lambda text, *rest: f'Utah School Board District {text}',
        search_key='utah school board district',
    ),
    Table(
        'opensgid.political.senate_districts_2022_to_2032',
        'dist',
        POLYGON,
        search_field_type=NUMERIC,
        get_suggestion_text_from_record=lambda text, *rest: f'Utah Senate District {text}',
        search_key='utah senate district',
    ),
    Table(
        'opensgid.political.us_congress_districts_2022_to_2032',
        'district',
        POLYGON,
        search_field_type=NUMERIC,
        get_suggestion_text_from_record=lambda text, *rest: f'Utah U.S. Congressional District {text}',
        search_key='utah us congress district'
    ),
    AddressPointTable('opensgid.location.address_points', FULLADD, POINT, additional_out_fields=[ADDSYSTEM, CITY]),
    Table(
        'opensgid.boundaries.county_boundaries',
        'name',
        POLYGON,
        get_suggestion_text_from_record=lambda text, *rest: f'{text.title()} County'
    ),
    Table('opensgid.boundaries.municipal_boundaries', 'name', POLYGON),
    Table('opensgid.boundaries.zip_code_areas', 'zip5', POLYGON, additional_out_fields=['name']),
    FullTextTable('opensgid.location.gnis_place_names', 'name', POINT),
]


def get_suggestions(search_text, max_results):
    """ queries the database and returns suggestions based on the input text
    """
    suggestions = []

    for table in TABLES:
        suggestions.extend(table.get_suggestions(search_text, max_results))

    return suggestions


def get_candidate_from_magic_key(magic_key, out_spatial_reference):
    """ queries the database for the feature corresponding to the magic key and
    returns it as an address candidate
    """
    xid, table_name = magic_key.split(SPLITTER)

    table = get_table_from_table_name(table_name)

    return table.get_candidate_from_magic_key(xid, out_spatial_reference)


def get_table_from_table_name(table_name):
    """ return the table object that matches the given table name
    """
    for table in TABLES:
        if table.table_name == table_name:
            return table

    raise NoTableFoundException(table_name)


class NoTableFoundException(Exception):
    """ raised when no table is found for a given table name
    """

    def __init__(self, table_name):
        super().__init__(f'No table found: {table_name}')
