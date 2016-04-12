# encoding: utf-8
"""Unit tests for the upload module."""
from os import path
import unittest

import upload

_TESTDATA_DIR = path.join(path.dirname(__file__), 'testdata')


class DataPrepareTestCase(unittest.TestCase):
    """Unit tests for data preparation methods/"""

    def test_csv_to_dicts(self):
        dicts = upload.csv_to_dicts(
            path.join(_TESTDATA_DIR, 'unix_referentiel_appellation.csv'),
            path.join(_TESTDATA_DIR, 'unix_referentiel_code_rome.csv'))

        self.assertEqual(9, len(dicts))
        for job in dicts:
            self.assertEqual([
                'codeOgr',
                'codeRome',
                'codeTypeSectionAppellation',
                'libelleAppellationCourt',
                'libelleAppellationLong',
                'libelleRome',
                'libelleTypeSectionAppellation',
                'statut',
            ], sorted(job.keys()))

        first_job = dicts[0]
        self.assertEqual(
            u'Abatteur / Abatteuse de carrière',
            first_job['libelleAppellationCourt'])
        # TODO: Make it a string and not an int.
        self.assertEqual(10200, first_job['codeOgr'])
        self.assertEqual('F1402', first_job['codeRome'])
        self.assertEqual('Extraction solide', first_job['libelleRome'])


if __name__ == '__main__':
    unittest.main()
