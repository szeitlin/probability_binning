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

    def count_index(self) -> dict:
        """
        Group by counts.

        :return self.invind: inverted index as a dict {counts: list of values that have those counts}

        """
        counts = Counter(self.df[self.feature])
        self.invind = {}
        for key, val in counts.items():
            self.invind.setdefault(val, []).append(key)

        #sort the values list
        for k,v in self.invind.items():
            if len(v) > 1:
                self.invind.update({k:sorted(v)})

    def bin_combiner(self, bins=3, toplot=False, debug=False):
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
        print("sum of counts: {}".format(count_target * bins))
        print("count target: {}".format(count_target))

        #sort by biggest_key and then by values
        biggest_key = sorted(list(prob.invind.items()), reverse=True)
        ordered = sorted(biggest_key, key=lambda x:x[1][0])

        newbins = dict()

        counts_list, value_list = [], []

        #combine bins if a) counts (keys) are the same or adjacent, b) values are sequential

        #take largest # of counts first

        tracker = ordered.copy()

        for counts,v in ordered:
            item = counts,v #to potentially use for tracking

            #stopping criteria
            if sum(counts_list) >= count_target:

                #adjust the bin sizes to be more permissive
                count_target = sum(counts_list)

                if toplot==True:
                    newbins[sum(counts_list)] = sum(value_list)/len(value_list) #use the mean as the center

                else:
                    newbins[sum(counts_list)] = [min(value_list), max(value_list)]
                counts_list, value_list = [], []

            elif sum(counts_list) < count_target:
                counts_list.append(counts)

                #append sequential values
                if len(v) == 1:
                    value_list.append(v[0]) #it's a list, have to index into it to get the contents
                    tracker.remove(item)
                elif len(v) == 2:
                    if v[1] - v[0] == 1:
                        value_list.extend(v)
                        tracker.remove(item)

                elif len(v) > 2:
                    tmp = pd.Series(v)
                    delta = tmp.diff()
                    if delta.max() == 1: #doing it this way handles NaNs correctly
                        value_list.extend(v)
                    else:
                        value_list.extend(tmp.where(delta==1).dropna().values)

        #todo: still need to add something to get rid of the used ones & use the remaining values
        print("remaining: {}". format(tracker))
        if len(tracker) > 0 and any([x < count_target for x in newbins.keys()]):
            #use any leftover ones here to expand the bin_ranges
            for k,v in tracker:
                #logic: find bin that is not > count_target
                        # then check to see if any values would fit that range or widen it

        #newbins[sum(counts_list)] = [min(value_list), max(value_list)]
        self.bin_ranges = sorted(newbins.values(), key=lambda x:x[0])

        print("bin sizes: {}".format([newbins]))


    def bin_masker(self):
        """
        Use bin_ranges from probability binning to create categorical column

        Should work for any number of bins > 0

        :param self.df: pandas dataframe as reference and target
        :param self.feature: reference column name (str) - will be used to create new one
        :param self.bin_ranges: sorted list of newbins, as bin ranges [min, max]
        :return: modified pandas dataframe with categorical column
        """
        masks = []

        for item in self.bin_ranges:
            mask = (self.df[self.feature] >= item[0]) & (self.df[self.feature] <= item[1])
            masks.append(mask)

        for i, mask in enumerate(masks):
            self.df.loc[mask, (self.feature + '_cat')] = i

        #may have to put something in to get the ones on the high end tail?

        self.df[self.feature + '_cat'].fillna(0, inplace=True) #if needed, get the bottom category

    def plot_with_newbins(self):
        """
        Make a plot using the newbins (output of bin_combiner with toplot=True)

        :return:(plot will show inline in jupyter notebook)
        """
        x = list(self.newbins.values())
        y = list(self.newbins.keys())
        plotframe = pd.DataFrame({"x":x, "y":y})

        return ggplot(aes(x="x", weight="y"), plotframe) + geom_bar()

if __name__ =='__main__':
    df = pd.read_csv("http://people.stern.nyu.edu/wgreene/Text/Edition7/TableF18-2.csv")
    # print(df.head())
    # prob = Probabinerator(df, 'INVC')
    # prob.count_index()
    # prob.bin_combiner(debug=True)
    # print("bin ranges: {}".format(prob.bin_ranges))
    # prob.bin_masker()

    print("try another column")
    prob = Probabinerator(df, 'TTME')
    prob.count_index()
    print("raw counts: {}".format(prob.invind))
    prob.bin_combiner(debug=True)
    print("bin ranges: {}".format(prob.bin_ranges))
    prob.bin_masker()
    print(prob.df.head())