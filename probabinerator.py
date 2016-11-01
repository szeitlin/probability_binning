__author__ = 'szeitlin'

from collections import Counter
import pandas as pd


class Probabinerator:
    """
    Create and apply categorical labels using probability binning.
    """

    def __init__(self, df, colname):
        """
        Initialize required inputs.

        :param df: source (and target) pandas dataframe
        :param colname: source column (str)
        """
        self.df = df
        self.feature = colname

    def count_index(self):
        """
        Group by counts.

        :return self.invind: inverted index as a dict {counts: list of values that have those counts}

        """
        counts = Counter(df[column])
        self.invind = {}
        for key, val in counts.items():
            self.invind.setdefault(val, []).append(key)

    def bin_combiner(self, bins=3, toplot=False):
        """
        Use probability binning approach to
        combine bins when invind has many bins with unequal counts

        :param invind: keys are number of counts,
        values are the range
        :param bins: number of bins to aim for, default is 3
        :return: list of lists (pairs) defining bin ranges
        """
        #sum the total number of counts, then divide equally into bins
        count_target = sum(list(self.invind.keys()))/bins

        newbins = dict()

        key_list, value_list = [],[]

        for key,value in sorted(list(self.invind.items()), key=lambda x: x[1][0]): #sort by values

            #when the list is full enough, spit it out and re-initialize to empty
            if sum(key_list) >= count_target:

                if toplot==True:
                    newbins[sum(key_list)] = sum(value_list)/len(value_list) #use the mean
                else:
                    newbins[sum(key_list)] = [min(value_list), max(value_list)]
                key_list, value_list = [], []

            #until the list fills up, keep appending
            if sum(key_list) < count_target:

                key_list.append(key)
                value_list.append(value[0])

        #need this if the last batch is not big enough
        if toplot==True:
            newbins[sum(key_list)] = sum(value_list)/len(value_list)
            self.newbins = newbins
        else:
            newbins[sum(key_list)] = [min(value_list), max(value_list)]
            self.bin_ranges = sorted(newbins.values(), key=lambda x:x[0])

    def