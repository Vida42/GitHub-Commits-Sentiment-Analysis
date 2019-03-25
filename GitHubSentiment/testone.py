#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-16 15:52:52
# @Author  : Amano
# @Version : $Id$



import os
import pandas as pd
import sqlite3 as sqlite
from texttable import Texttable
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm

# get main project path (in case this file is compiled alone)


db_location = './vader_databse.db'
db_connection = sqlite.connect(db_location)


def EmotionsTeamDistribution():
    print("Emotions and project approval：\n")

    location = {}
    top6 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_com, location FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] in projectEmotion:
            projectEmotion[row['project_name']].append(float(row['sentiment_com']))
        else:
            projectEmotion[row['project_name']] = [float(row['sentiment_com'])]


    count = 0
    for item in df['location'].tolist():
        if item is not None:
            item_encode = item.encode('utf-8')

            split1 = item_encode.split(',')
            split2 = item_encode.split('-')
            split3 = item_encode.split(' ')

            if len(split1) > 1:
                print(split1[-1])

            elif len(split2) > 1:
                print(split2[-1])

            elif len(split3) > 1:
                print(split3[-1])

            else:
                print(item_encode)

        count += 1
        if count == 50:
            break;