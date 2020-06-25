import os
import unittest

import pandas as pd
import pandas.api.types as ptypes

import populate


class TestPopulate(unittest.TestCase):
    dirname = os.path.dirname(__file__)
    filename = 'test.zip'
    url = 'file:' + os.path.join(dirname, filename)

    def test_get_zip_file(self):
        res = populate.get_zip_file(self.url)
        # must return byte stream
        self.assertTrue(isinstance(res, bytes))
        # must match the size of the sample file
        self.assertEqual(os.stat('tests/' + self.filename).st_size, len(res))

    def test_data_from_zip(self):
        with open('tests/pc6hnr.csv', 'rb') as f:
            res = populate.data_from_zip(f.read())
            # must return a DF
            self.assertTrue(isinstance(res, pd.DataFrame))
            # pc6 must be unique
            self.assertTrue(res['pc6'].is_unique)
            # must contain the following columns
            self.assertListEqual(['pc6', 'buurt', 'wijk', 'gemeente'], list(res.columns))
            # must have the correct data types
            self.assertTrue(ptypes.is_string_dtype(res['pc6']))
            self.assertTrue(all(ptypes.is_int64_dtype(res[col]) for col in ['buurt', 'wijk', 'gemeente']))


if __name__ == '__main__':
    unittest.main()
