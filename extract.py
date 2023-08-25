"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        neos = [NearEarthObject(neo['pdes'], neo['name'], neo['diameter'], neo['pha']) for neo in reader]

    return neos

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    """fields in json file: signature, count, fields, data"""
    with open(cad_json_path, 'r') as jsonfile:
        data = json.load(jsonfile)

    fields = data['fields']
    des_index = fields.index('des')
    time_index = fields.index('cd')
    dist_index = fields.index('dist')
    velocity_index = fields.index('v_rel')
    close_approaches = [CloseApproach(ca[time_index], ca[dist_index], ca[velocity_index], ca[des_index], None) for ca in data['data']]

    return close_approaches 

