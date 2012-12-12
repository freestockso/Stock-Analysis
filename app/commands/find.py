#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
$ stock find 610001
[
    {"date":"2011-11-10" , "strategic":"xxx"  , "bayes":" ", "markov":"" , "reporter":""},
    ...
]
"""
from stk import Finder

def run(conf = conf):
    finder = Finder(conf =conf )
    return finder.find()
