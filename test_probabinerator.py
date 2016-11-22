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
        #assert that values are in order

    def test_bin_combiner_result_type(self):
        """
        use defaults first
        """
        self.prob.bin_combiner()
        assert(all([isinstance(x, list) for x in self.prob.bin_ranges]))

    def test_bin_combiner_no_missing_segments(self):
        """
        Check remaining values in kv_list to make sure bin_combiner didn't leave any out
        :return:
        """
        #logic is to check that remaining values do not get lost between (or outside) the existing bin_ranges
        print(self.prob.invind)
        remaining_keys = self.prob.bin_combiner(debug=True)
        for item in remaining_keys:
            print(item)

        #for TTME column, missing 99 (far right) and 40 (between two bins)

    def test_bin_combiner_no_weird_combinations(self):
        """
        What to do about ones like this, where the values are not adjacent?

        {1: [1, 2, 16, 80, 85]}
        :return:
        """
        pass

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
