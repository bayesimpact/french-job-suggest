"""Script to upload job suggestions to Algolia.

It relies on environment variables to be set correctly:
    ALGOLIA_APP_ID: the Algolia App to update
    ALGOLIA_JOB_INDEX: the index to update in this App
    ALGOLIA_API_KEY: an API key that has enough permissions to edit the index.

The script takes one argument: a path to the csv file containing the definition
of jobs in the ROME.
"""
import os
import sys

from algoliasearch import algoliasearch
import pandas

_CLIENT = algoliasearch.Client(
    os.getenv('ALGOLIA_APP_ID'), os.getenv('ALGOLIA_API_KEY'))
_JOB_INDEX = _CLIENT.init_index(os.getenv('ALGOLIA_JOB_INDEX', 'jobs'))


def upload(csv_filename):
    """Upload jobs suggestions to Algolia."""
    suggestions = pandas.read_csv(csv_filename)
    _JOB_INDEX.clear_index()
    _JOB_INDEX.add_objects(suggestions.to_dict(orient='records'))


if __name__ == '__main__':
    upload(*sys.argv[1:])
