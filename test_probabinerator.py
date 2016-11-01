__author__ = 'szeitlin'

import pytest
from probabinerator import Probabinerator

import pandas as pd

@pytest.fixture()
def before():
    print('\nbefore each test')
    prob = Probabinerator()

def test_probabinerator(prob):

    assert(isinstance(prob.df, pd.DataFrame))