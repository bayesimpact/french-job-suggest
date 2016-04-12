"""Script to upload job suggestions to Algolia.

It relies on environment variables to be set correctly:
    ALGOLIA_APP_ID: the Algolia App to update
    ALGOLIA_JOB_INDEX: the index to update in this App
    ALGOLIA_API_KEY: an API key that has enough permissions to edit the index.

The script takes two arguments:
 - a path to the csv file containing the definition of jobs in the ROME,
 - a path to the csv file containing the definition of job groups in the ROME.
"""
import json
import os
import sys

from algoliasearch import algoliasearch
from algoliasearch import helpers
import pandas

_CLIENT = algoliasearch.Client(
    os.getenv('ALGOLIA_APP_ID'), os.getenv('ALGOLIA_API_KEY'))
_JOB_INDEX = _CLIENT.init_index(os.getenv('ALGOLIA_JOB_INDEX', 'jobs'))


def csv_to_dicts(csv_appellation, csv_code_rome):
    appellations = pandas.read_csv(csv_appellation)
    appellations['code_ogr'] = appellations['code_ogr'].astype(str)
    code_rome = pandas.DataFrame(
        pandas.read_csv(csv_code_rome),
        columns=['code_rome', 'libelle_rome'])
    suggestions = pandas.merge(
        appellations, code_rome,
        left_on='code_rome', right_on='code_rome', how='left')
    return suggestions.to_dict(orient='records')


def upload(csv_appellation, csv_code_rome):
    """Upload jobs suggestions to Algolia."""
    suggestions = csv_to_dicts(csv_appellation, csv_code_rome)
    try:
        _JOB_INDEX.clear_index()
        _JOB_INDEX.add_objects(suggestions)
    except helpers.AlgoliaException:
        print(json.dumps(suggestions[:10], indent=2))
        raise


if __name__ == '__main__':
    upload(*sys.argv[1:])
