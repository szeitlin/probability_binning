__author__ = 'szeitlin'

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

    def test_probabinerator_df(self):

        assert(isinstance(self.prob.df, pd.DataFrame))

    def test_probabinerator_feature(self):

        assert(isinstance(self.prob.df[self.prob.feature], pd.Series))



if '__name__'=='__main__':
    import pytest
    pytest.main()
