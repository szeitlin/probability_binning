__author__ = 'szeitlin'

#to run with pytest: py.test -v <filename>

from probabinerator import Probabinerator

import pandas as pd

class TestProbabinerator:

    @classmethod
    def setup_class(cls):
        """
        Uses a publicly-available dataset for regression testing
        """
        print('runs once')
        df = pd.read_csv("http://people.stern.nyu.edu/wgreene/Text/Edition7/TableF18-2.csv")
        cls.prob = Probabinerator(df, 'INVC')

    def test_probabinerator_df_type(self):

        assert(isinstance(self.prob.df, pd.DataFrame))

    def test_probabinerator_feature_type(self):

        assert(isinstance(self.prob.df[self.prob.feature], pd.Series))

    def test_count_index_types(self):
        self.prob.count_index()
        assert(isinstance(self.prob.invind, dict))
        assert(all([isinstance(x, list) for x in list(self.prob.invind.values())]))

    def test_bin_combiner_result_type(self):
        """
        use defaults first
        """
        self.prob.bin_combiner()
        assert(all([isinstance(x, list) for x in self.prob.bin_ranges]))

    def test_bin_masker(self):
        """
        Need to make sure results make sense!

        """
        self.prob.bin_masker()
        #assert that value_counts for the _cat column are correct
        #assert that the 0.0 cat does not include both min and max values


if __name__=='__main__':

    #Not sure if this actually works or not

    import pytest
    pytest.main()
