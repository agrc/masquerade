#!/usr/bin/env python
# * coding: utf8 *
"""
A provider that queries data in Open SGID
"""
import psycopg2
from shapely import wkt

FULL_ADDRESS_FIELD = 'fulladd'
OBJECTID = 'xid'
ADDRESS_SYSTEM_FIELD = 'addsystem'
CITY_FIELD = 'city'
DATABASE = 'opensgid'
AGRC = 'agrc'
HOST = 'opensgid.agrc.utah.gov'
ADDRESS_POINTS_TABLE = 'opensgid.location.address_points'

connection = psycopg2.connect(database=DATABASE, user=AGRC, password=AGRC, host=HOST)
out_fields = [OBJECTID, FULL_ADDRESS_FIELD, ADDRESS_SYSTEM_FIELD, CITY_FIELD]


def get_suggestion_from_record(oid, full_address, address_system, city):
    """ return a suggestion dictionary based on a database record
    """
    if city is not None:
        zone = city
    else:
        zone = address_system

    return {'isCollection': False, 'magicKey': oid, 'text': f'{full_address}, {zone}'}


def get_suggestions(search_text):
    """ queries the feature service and returns suggestions based on the input text
    """
    query = f'''
        select {','.join(out_fields)} from {ADDRESS_POINTS_TABLE}
        where upper({FULL_ADDRESS_FIELD}) LIKE upper(\'{search_text}%\')
        order by {FULL_ADDRESS_FIELD} ASC
        limit 50
    '''

    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()

    return [get_suggestion_from_record(*record) for record in records]


def get_candidate_from_magic_key(magic_key, out_spatial_reference):
    """ queries the database for the feature corresponding to the magic key and
    returns it as an address candidate
    """
    shape = f'ST_AsText(ST_Transform(shape, {out_spatial_reference}))'
    query = f'''
        select {','.join(out_fields + [shape])} from {ADDRESS_POINTS_TABLE}
        where {OBJECTID} = {magic_key}
    '''

    cursor = connection.cursor()
    cursor.execute(query)
    record = cursor.fetchone()

    geometry = wkt.loads(record[-1])

    #: todo - handle out spatial reference

    return {
        'address': get_suggestion_from_record(*record[:-1])['text'],
        'attributes': {
            'score': 100
        },
        'location': {
            # pylint: disable=no-member
            'x': geometry.x,
            'y': geometry.y
        }
    }
