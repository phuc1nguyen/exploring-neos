"""Transform and simplify given data set into CSV files.

Create new file that has only necessary fields.
"""
import csv
import json


def load_neos(neo_csv_path='./data/neos.csv'):
    selected_fields = ['pdes', 'name', 'diameter', 'pha']

    with open(neo_csv_path, 'r') as in_csv:
        reader = csv.DictReader(in_csv)
        list_of_neos = []
        for row in reader:
            list_of_neos.append(row)
        mini_list_of_neos = [dict(
            (key, neo[key]) for key in selected_fields if key in neo) for neo in list_of_neos]

    with open('./data/mini_neos.csv', 'w') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=selected_fields)
        writer.writeheader()
        writer.writerows(mini_list_of_neos)


def load_approaches(cad_json_path='./data/cad.json'):
    selected_fields = ['des', 'cd', 'dist', 'v_rel']

    with open(cad_json_path, 'r') as in_json:
        json_data = json.load(in_json)
        list_of_close_approaches = [
            dict(zip(json_data['fields'], data)) for data in json_data['data']]
        mini_list_of_close_approaches = [
            dict((key, ca[key]) for key in selected_fields if key in ca)
            for ca in list_of_close_approaches
        ]

    with open('./data/mini_cad.csv', 'w') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=selected_fields)
        writer.writeheader()
        writer.writerows(mini_list_of_close_approaches)
