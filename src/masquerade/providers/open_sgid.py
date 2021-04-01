#!/usr/bin/env python
# * coding: utf8 *
"""
A provider that queries data in Open SGID
"""
import re

import psycopg2

DATABASE = 'opensgid'
AGRC = 'agrc'
HOST = 'opensgid.agrc.utah.gov'
SPLITTER = '-'
POINT = 'point'
POLYGON = 'polygon'

#: field names
XID = 'xid'
FULLADD = 'fulladd'
ADDSYSTEM = 'addsystem'
CITY = 'city'
NAME = 'name'

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


class DatabaseConnection():
    """ used to interact with the open sgid database
    """

    def __init__(self) -> None:
        self.connection = self.ensure_open()

    def ensure_open(self):
        """ get an always-open connection
        """

        #: closed == 0 means it is open, anything else, it's closed
        if not hasattr(self, 'connection') or self.connection.closed != 0:
            return psycopg2.connect(database=DATABASE, user=AGRC, password=AGRC, host=HOST)

        return self.connection

    def query(self, query):
        """ get records from the database
        """
        cursor = self.ensure_open().cursor()
        cursor.execute(query)

        return cursor.fetchall()


database = DatabaseConnection()


class Table():
    """ object that orchestrates communication with a specific table in open sgid
    """
    SPLITTER = '-'

    def __init__(self, table_name, search_field, additional_out_fields, geometry_type):
        self.table_name = table_name
        self.search_field = search_field
        self.additional_out_fields = additional_out_fields
        self.geometry_type = geometry_type

    def get_suggestion_from_record(self, xid, match_text, context_value=None):
        """ return a suggestion dictionary based on a database record
        """
        if context_value:
            match_text = f'{match_text}, {context_value}'

        return self.make_suggestion(xid, match_text)

    def make_suggestion(self, xid, match_text):
        """ return a suggestion dictionary based on the id and match text
        """
        return {'isCollection': False, 'magicKey': f'{xid}{self.SPLITTER}{self.table_name}', 'text': match_text}

    def get_suggest_query(self, search_text, limit):
        """ create a query that returns records for suggestions
        """
        return f'''
            select {self.get_out_fields()} from {self.table_name}
            where {self.search_field} ilike \'{search_text}%\'
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
        records = database.query(self.get_suggest_query(search_text, max_results))

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
            select {f'{self.get_out_fields()}, {shape}'} from {self.table_name}
            where {XID} = {xid}
        '''

    def get_candidate_from_magic_key(self, xid, out_spatial_reference):
        """ returns a candidate dictionary with the data corresponding to the value that matches the xid value
        """
        record = database.query(self.get_magic_key_query(xid, out_spatial_reference))[0]
        x_value, y_value, xmax, ymax, xmin, ymin = record[-6:]

        return {
            'text': self.get_suggestion_from_record(*record[:-6])['text'],
            'score': 100,
            'location': {
                'x': x_value,
                'y': y_value
            },
            'attributes': {
                'Score': 100,
                'X': x_value,
                'Y': y_value,
            },
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

    # pylint: disable=arguments-differ
    #: I'm not worries about this because the call to this method unpacks it's arguments
    def get_suggestion_from_record(self, xid, full_address, address_system, city):
        """ return a suggestion dictionary based on a database record
        """
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


TABLES = [
    AddressPointTable('opensgid.location.address_points', FULLADD, [ADDSYSTEM, CITY], POINT),
    Table('opensgid.boundaries.county_boundaries', 'name', [], POLYGON),
    Table('opensgid.boundaries.municipal_boundaries', 'name', [], POLYGON),
    Table('opensgid.boundaries.zip_code_areas', 'zip5', ['name'], POLYGON),
    Table('opensgid.location.gnis_place_names', 'name', [], POINT)
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

    raise Exception(f'No table found: {table_name}')
