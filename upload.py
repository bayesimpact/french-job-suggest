"""Script to upload job suggestions to Algolia.

It relies on environment variables to be set correctly:
    ALGOLIA_APP_ID: the Algolia App to update
    ALGOLIA_JOB_INDEX: the index to update in this App
    ALGOLIA_API_KEY: an API key that has enough permissions to edit the index.

The script takes two arguments:
 - a path to the csv file containing the definition of jobs in the ROME,
 - a path to the csv file containing the definition of job groups in the ROME,
 - a path to the file with correspondance from ROME job group to FAP codes,
 - a path to the JSON file with job frequencies.
"""
import codecs
import json
import os
import re
import sys

from algoliasearch import algoliasearch
from algoliasearch import helpers
import pandas

# Regular expression to match mapping of ROME to FAP codes.
# Matches strings like '"A1201","A1205"   =   "A0Z42"'
_ROME_FAP_MAPPING_REGEXP = re.compile(
    r'^(?P<rome_ids>(?:"[A-Z]\d{4}",?)+)\s*=\s*"(?P<fap>[A-Z]\d[A-Z]\d\d)"$')


def csv_to_dicts(
        csv_appellation, csv_code_rome, txt_fap_rome, json_jobs_frequency):
    # Read appellations from CSV.
    appellations = pandas.read_csv(csv_appellation)
    appellations['code_ogr'] = appellations['code_ogr'].astype(str)

    # Join with ROME names.
    code_rome = pandas.DataFrame(
        pandas.read_csv(csv_code_rome),
        columns=['code_rome', 'libelle_rome'])
    suggestions = pandas.merge(
        appellations, code_rome, on='code_rome', how='left')

    # Join with FAP code when simple.
    rome_to_fap = _fap_rome_simple_mapping(txt_fap_rome)
    suggestions = pandas.merge(
        suggestions, rome_to_fap, on='code_rome', how='left')

    # Join with jobs frequency from exernal file.
    with open(json_jobs_frequency) as jobs_frequency_file:
        jobs_frequency = json.load(jobs_frequency_file)
    suggestions['frequency'] = (
        suggestions['code_ogr'].map(jobs_frequency).fillna(0))

    # Swith properties to camelCase.
    mapping = {
        name: _snake_to_camel_case(name)
        for name in suggestions.columns.tolist()}
    suggestions.rename(columns=mapping, inplace=True)

    # Convert from pandas.DataFrame to Python list of dicts.
    records = suggestions.to_dict(orient='records')
    return [{k: v for k, v in record.items() if not pandas.isnull(v)}
            for record in records]


def upload(csv_appellation, csv_code_rome, txt_fap_rome, json_jobs_frequency):
    """Upload jobs suggestions to Algolia."""
    suggestions = csv_to_dicts(
        csv_appellation, csv_code_rome, txt_fap_rome, json_jobs_frequency)
    client = algoliasearch.Client(
        os.getenv('ALGOLIA_APP_ID'), os.getenv('ALGOLIA_API_KEY'))
    job_index = client.init_index(os.getenv('ALGOLIA_JOB_INDEX', 'jobs'))
    try:
        job_index.clear_index()
        job_index.add_objects(suggestions)
    except helpers.AlgoliaException:
        print(json.dumps(suggestions[:10], indent=2))
        raise


def _snake_to_camel_case(snake_name):
    components = snake_name.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def _fap_rome_simple_mapping(txt_fap_rome):
    """Return mappings from ROME to FAP when non ambiguous.

    Many ROME job groups are included completely in one FAP group, so for them
    a mapping is possible from ROME ID to FAP. This function extract those
    simple mappings.

    Args:
        txt_fap_rome: path of a file containing the official mapping.
    Returns:
        a pandas DataFrame with two columns: "code_rome" and "code_fap".
    """
    mapping = []
    with codecs.open(txt_fap_rome, 'r', 'latin-1') as fap_rome:
        for line in fap_rome:
            matches = _ROME_FAP_MAPPING_REGEXP.match(line.strip())
            if not matches:
                continue
            rome_ids_str = matches.group('rome_ids')
            # Splitting and removing quotes from: "A1201","A1205","A1206"
            rome_ids = rome_ids_str[1:len(rome_ids_str)-1].split('","')
            fap_id = matches.group('fap')
            for rome_id in rome_ids:
                mapping.append((rome_id, fap_id))
    mapping_df = pandas.DataFrame(mapping)
    mapping_df.columns = ['code_rome', 'code_fap']
    return mapping_df


if __name__ == '__main__':
    upload(*sys.argv[1:])
