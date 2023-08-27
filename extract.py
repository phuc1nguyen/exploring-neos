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
    with open(neo_csv_path, 'r') as in_csv:
        reader = csv.DictReader(in_csv)
        neos = []

        for row in reader:
            pdes = str(row['pdes'])
            name = str(row['name']) or None
            diameter = float(
                row['diameter']) if row['diameter'] else float('nan')
            pha = True if row['pha'] == 'Y' else False

            neo = NearEarthObject(
                designation=pdes,
                name=name,
                diameter=diameter,
                hazardous=pha
            )
            neos.append(neo)

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as in_json:
        json_data = json.load(in_json)
        list_of_close_approaches = [
            dict(zip(json_data['fields'], data)) for data in json_data['data']]
        close_approaches = []

        for approach in list_of_close_approaches:
            des = str(approach['des'])
            cd = str(approach['cd'])
            dist = round(float(approach['dist']), 2)
            v_rel = round(float(approach['v_rel']), 2)

            ca = CloseApproach(
                designation=des,
                time=cd,
                distance=dist,
                velocity=v_rel
            )
            close_approaches.append(ca)

    return close_approaches
