#!/usr/bin/env python
# * coding: utf8 *
"""
A provider that queries data in Open SGID
"""
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

connection = psycopg2.connect(database=DATABASE, user=AGRC, password=AGRC, host=HOST)


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
        cursor = connection.cursor()
        cursor.execute(self.get_suggest_query(search_text, max_results))
        records = cursor.fetchall()

        return [self.get_suggestion_from_record(*record) for record in records]

    def get_magic_key_query(self, xid, out_spatial_reference):
        """ create a query for getting a specific record using the xid value

        Also translates the geometry into x, y and extent fields.
        """
        if self.geometry_type == POINT:
            extent = f'st_expand(st_transform(shape, {out_spatial_reference}), 500)'
        else:
            extent = f'st_transform(shape, {out_spatial_reference})'

        shape = f'''
            st_x(st_transform(st_centroid(shape), {out_spatial_reference})) as x,
            st_y(st_transform(st_centroid(shape), {out_spatial_reference})) as y,
            st_xmax({extent}) as xmax,
            st_ymax({extent}) as ymax,
            st_xmin({extent}) as xmin,
            st_ymin({extent}) as ymin
        '''

        return f'''
            select {f'{self.get_out_fields()}, {shape}'} from {self.table_name}
            where {XID} = {xid}
        '''

    def get_candidate_from_magic_key(self, xid, out_spatial_reference):
        """ returns a candidate dictionary with the data corresponding to the value that matches the xid value
        """
        cursor = connection.cursor()
        cursor.execute(self.get_magic_key_query(xid, out_spatial_reference))
        record = cursor.fetchone()
        x_value, y_value, xmax, ymax, xmin, ymin = record[-6:]

        return {
            'text': self.get_suggestion_from_record(*record[:-6])['text'],
            'attributes': {
                'score': 100
            },
            'extent': {
                'xmax': xmax,
                'xmin': xmin,
                'ymax': ymax,
                'ymin': ymin
            },
            'location': {
                'x': x_value,
                'y': y_value
            }
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
