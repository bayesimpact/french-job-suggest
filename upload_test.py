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
            path.join(_TESTDATA_DIR, 'unix_referentiel_code_rome.csv'),
            path.join(_TESTDATA_DIR, 'passage_fap2009_romev3.txt'),
            path.join(_TESTDATA_DIR, 'jobs_frequency.json'))

        self.assertEqual(11, len(dicts))
        for job in dicts:
            keys = set(job.keys()) - set(['codeFap'])
            self.assertEqual([
                'codeOgr',
                'codeRome',
                'codeTypeSectionAppellation',
                'frequency',
                'libelleAppellationCourt',
                'libelleAppellationCourtFeminin',
                'libelleAppellationCourtMasculin',
                'libelleAppellationLong',
                'libelleAppellationLongFeminin',
                'libelleAppellationLongMasculin',
                'libelleRome',
                'libelleTypeSectionAppellation',
                'statut',
            ], sorted(keys))

        first_job = dicts[0]
        self.assertEqual(
            u'Abatteur / Abatteuse de carrière',
            first_job['libelleAppellationCourt'])
        self.assertEqual(
            u'Abatteuse de carrière',
            first_job['libelleAppellationCourtFeminin'])
        self.assertEqual(
            u'Abatteur de carrière',
            first_job['libelleAppellationCourtMasculin'])
        self.assertEqual('10200', first_job['codeOgr'])
        self.assertEqual('F1402', first_job['codeRome'])
        self.assertNotIn('codeFap', first_job)
        self.assertEqual('Extraction solide', first_job['libelleRome'])
        self.assertEqual(42, first_job['frequency'])

        self.assertEqual('Accessoiriste', dicts[3]['libelleAppellationCourt'])
        self.assertEqual('U1Z80', dicts[3]['codeFap'])
        self.assertEqual('L1503', dicts[3]['codeRome'])
        self.assertEqual(0, dicts[3]['frequency'])

        self.assertEqual(u'Égoutier / Égoutière', dicts[10]['libelleAppellationCourt'])
        self.assertEqual(u'Égoutier / Égoutière', dicts[10]['libelleAppellationLong'])
        self.assertEqual(u'Égoutier', dicts[10]['libelleAppellationCourtMasculin'])


if __name__ == '__main__':
    unittest.main()
