__author__ = 'szeitlin'

from collections import Counter
import pandas as pd
from ggplot import *

class Probabinerator:
    """
    Create and apply categorical labels using probability binning.
    """

    def __init__(self, df: pd.DataFrame, colname:str) -> None:
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
        counts = Counter(self.df[self.feature])
        self.invind = {}
        for key, val in counts.items():
            self.invind.setdefault(val, []).append(key)

    def bin_combiner(self, bins=3, toplot=False):
        """
        Use probability binning approach to
        combine bins when invind has many bins with unequal counts

        :param self.invind: keys are number of counts,
        values are the range
        :param bins: number of bins to aim for (int), default is 3
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

    def bin_masker(self):
        """
        Use bin_ranges from probability binning to create categorical column

        Should work for any number of bins > 0

        :param self.df: pandas dataframe as reference and target
        :param self.feature: reference column name (str) - will be used to create new one
        :param self.bin_ranges: sorted list of newbins, only care about using the values as bin ranges [min, max]
        :return: modified pandas dataframe with categorical column
        """
        masks = []

        for item in self.bin_ranges:
            mask = (self.df[self.feature] >= item[0]) & (self.df[self.feature] < item[1])
            masks.append(mask)

        for i, mask in enumerate(masks):
            self.df.loc[mask, (self.feature + '_cat')] = i
            self.df[self.feature + '_cat'].fillna(0, inplace=True) #get the bottom category

    def plot_with_newbins(self):
        """
        Make a plot using the newbins (output of bin_combiner with toplot=True)

        :return:(plot will show inline in jupyter notebook)
        """
        x = list(self.newbins.values())
        y = list(self.newbins.keys())
        plotframe = pd.DataFrame({"x":x, "y":y})

        return ggplot(aes(x="x", weight="y"), plotframe) + geom_bar()

if '__name__'=='__main__':
    prob = Probabinerator() #<-- requires dummy data for testing
    prob.count_index()
    prob.bin_combiner()
    prob.bin_masker()
