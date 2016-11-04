__author__ = 'szeitlin'

==================
**Probabinerator**
==================

*Simple univariate classification based on counts.*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Author**

Samantha G. Zeitlin

email: firstnamelastname@gmail

**License**: MIT
see `license.md <https://github.com/szeitlin/probability_binning/blob/master/license.md>`_

============================
What is probability binning?
============================

It's a way of grouping, i.e for a histogram or classification, where bin ranges are chosen to equalize the number of events per bin.

I didn't invent this approach. I learned about it from `this article <http://onlinelibrary.wiley.com/doi/10.1002/1097-0320(20010901)45:1%3C37::AID-CYTO1142%3E3.0.CO;2-E/full>`_ and wrote `a blog post with some very simple examples <http://codrspace.com/szeitlin/probability-binning-simple-and-fast/>`_. I previously used it in `one of my scientific publications <https://www.ncbi.nlm.nih.gov/pubmed/21399697>`_.

===============
When to use it:
===============

To convert a numeric, non-continuous variable into categories.

Use probability binning when you want a small number of approximately equal classes, defined in a way that makes sense, e.g. combine adjacent bins if they're similar.

For example, let's say you're looking at user data where every row is a separate user. The values of a specific column, say "Total clicks", might be numeric, but the users are independent of each other. In this case, what you really want to do is identify categories of users based on their number of clicks.
