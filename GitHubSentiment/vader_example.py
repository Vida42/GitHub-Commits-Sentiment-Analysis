#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-16 14:14:42
# @Author  : Amano
# @Version : $Id$

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

view2 = ["Great place to be when you are in Bangalore",
        "The place was being renovated when I visited so the seating was limited",
        "Loved the ambience, loved the food",
        "The place is not easy to locate"]

view = ["Well my fix was almost exactly the same (I used m_originalCasterGUID instead), so I guess the above mentioned tickets can be closed."]

sid = SentimentIntensityAnalyzer()

for sentence in view:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()