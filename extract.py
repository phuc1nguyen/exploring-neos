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


def load_neos(neo_csv_path='./data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    selected_fields = ['pdes', 'name', 'diameter', 'pha']

    with open(neo_csv_path, 'r') as in_csv:
        reader = csv.DictReader(in_csv)
        list_of_neos = []
        for row in reader:
            list_of_neos.append(dict(row))
        mini_list_of_neos = [dict((key, neo[key]) for key in selected_fields if key in neo) for neo in list_of_neos]

    with open('./data/mini_neos.csv', 'w') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=selected_fields)
        writer.writeheader()
        writer.writerows(mini_list_of_neos)

    with open('./data/mini_neos.csv', 'r') as in_csv:
        reader = csv.DictReader(in_csv)
        neos = [NearEarthObject(**row) for row in reader]

    return neos

def load_approaches(cad_json_path='./data/cad.json'):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    selected_fields = ['des', 'cd', 'dist', 'v_rel']

    with open(cad_json_path, 'r') as in_json:
        json_data = json.load(in_json)
        list_of_close_approaches = [dict(zip(json_data['fields'], data)) for data in json_data['data']]
        mini_list_of_close_approaches = [
            dict((key, ca[key]) for key in selected_fields if key in ca)
            for ca in list_of_close_approaches 
        ]

    with open('./data/mini_cad.csv', 'w') as out_csv:
       csv_writer = csv.DictWriter(out_csv, fieldnames=selected_fields)
       csv_writer.writeheader()
       csv_writer.writerows(mini_list_of_close_approaches)

    with open('./data/mini_cad.csv', 'r') as in_csv:
        reader = csv.DictReader(in_csv)
        close_approaches = [CloseApproach(**row) for row in reader]

    return close_approaches

