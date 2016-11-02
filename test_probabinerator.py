__author__ = 'szeitlin'

from probabinerator import Probabinerator

import pandas as pd

class TestProbabinerator:

    @classmethod
    def setup_class(cls):
        print('runs once')
        df =
        cls.prob = Probabinerator()

    def test_probabinerator(self):

        assert(isinstance(self.prob.df, pd.DataFrame))