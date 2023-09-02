"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import os
import csv
import json


out_dir = './outfiles'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(f"{out_dir}/{filename}", 'w') as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
        if results:
            contents = [dict(**ca.serialize(), **ca.neo.serialize())
                        for ca in results]
            writer.writeheader()
            writer.writerows(contents)
        else:
            writer.writeheader()


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(f"{out_dir}/{filename}", 'w') as out_json:
        if results:
            contents = [{**ca.serialize(), "neo": {**ca.neo.serialize()}}
                        for ca in results]
            json.dump(contents, out_json)
        else:
            json.dump([], out_json)
