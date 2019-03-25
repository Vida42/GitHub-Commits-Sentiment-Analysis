#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-17 13:59:24
# @Author  : Amano
# @Version : $Id$

# import tools
import os
import pandas as pd
import sqlite3 as sqlite
from texttable import Texttable
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import norm


# get main project path
db_location = './vader_databse.db'
db_connection = sqlite.connect(db_location)

# Principle in total

# assume table is a list of dictionaries
# get data from table
# import to pandas
# use pandas for displaying statistical data, and display bar graph
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html


# PAPER: Part A of Section 3.1
# Figure 1: Emotion score average per project.

# -----------------------------------------------------------------------------
# | Project    |  Commits   |     Mean    |   Stand. Dev.     |   p-value     |
# -----------------------------------------------------------------------------

def EmotionsProject():

    print( "Average Emotion Score per Project top10:\n")

    projectEmotion = {}
    top10 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_com FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] in projectEmotion:
            projectEmotion[row['project_name']].append(float(row['sentiment_com']))
        else:
            projectEmotion[row['project_name']] = [float(row['sentiment_com'])]

    for key in sorted(projectEmotion,  key=lambda k: len(projectEmotion[k]), reverse=True)[:10]:
        commits = len(projectEmotion[key])
        mean = stats.tmean(projectEmotion[key])
        std_dev = stats.tstd(projectEmotion[key])
        wilcoxon_test = stats.wilcoxon(projectEmotion[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        else:
            wilcoxon_test = wilcoxon_test[1]
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print('Wilcoxon p-value:', wilcoxon_test)    # Get p-value
        top10.append([key, commits, mean, std_dev, wilcoxon_test])


    t = Texttable()
    t.add_rows([['Project', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + top10)
    print (t.draw())

    print ("Top 10\n")

    objects = [val[0] for val in top10]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in top10]

    colors = ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k', 'k']
    plt.figure(figsize  = (12,4))
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors, width = 0.6)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 1. Emotion Score Average Per Project')

    plt.show()

    return top10

# PAPER: Part B of Section 3.1
# Figure 2: Proportion of positive, neutral and negative commit comments per project.

# --------------------------------------------------------------
# | Project    |  Negative   |     Neutral    |   Positive     |
# --------------------------------------------------------------

def EmotionsProjectProportion():
    print("Proportion of Emotion scores per project top10:\n")

    projectEmotion = {}
    # projectEmotion = {'negative':0, 'neutral':0, 'positive':0}
    top10 = []

    df = pd.read_sql_query("SELECT project_name, sentiment_com FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_name'] not in projectEmotion:
            projectEmotion[row['project_name']] = {'negative':[], 'neutral':[], 'positive':[]}

        emotion = float(row['sentiment_com'])
        if emotion < -0.1:
            projectEmotion[row['project_name']]['negative'].append(emotion)
        elif emotion > 0.1:
            projectEmotion[row['project_name']]['positive'].append(emotion)
        else:
            projectEmotion[row['project_name']]['neutral'].append(emotion)

    for key in sorted(projectEmotion,  key=lambda k: (len(projectEmotion[k]['negative']) + len(projectEmotion[k]['neutral']) + len(projectEmotion[k]['positive'])), reverse=True)[:10]:

        neg_val = float(len(projectEmotion[key]['negative'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))
        neut_val = float(len(projectEmotion[key]['neutral'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))
        pos_val = float(len(projectEmotion[key]['positive'])) / float(len(projectEmotion[key]['negative']) + len(projectEmotion[key]['neutral']) + len(projectEmotion[key]['positive']))

        top10.append([key, neg_val, neut_val, pos_val])


    t = Texttable()
    t.add_rows([['Project', 'Negative', 'Neutral', 'Positive']] + top10)
    print(t.draw())

    print("Proportion of positive, neutral and negative commit comments per project\n")

    objects = [val[0] for val in top10]
    y_pos = np.arange(len(objects))

    neg_avg =       [val[1] for val in top10]
    neutral_avg =   [val[2] for val in top10]
    pos_avg =       [val[3] for val in top10]

    # Stacked Bar(explanation of bottom Parameters)
    # https://blog.csdn.net/rose_424/article/details/78340390
    plt.figure(figsize  = (12,4))
    p3 = plt.bar(y_pos, pos_avg, align='center', color='m', width = 0.6)
    p2 = plt.bar(y_pos, neutral_avg, align='center', bottom=pos_avg, color='grey', width = 0.6)
    cum = list(map(sum, zip(list(pos_avg),list(neutral_avg))))
    p1 = plt.bar(y_pos, neg_avg, align='center', bottom=cum, color='k', width = 0.6)

    plt.xticks(y_pos, objects)
    plt.title('Fig 2. Proportion of positive, neutral and negative commit comments per project')
    plt.legend((p1[0], p2[0], p3[0]), ('Negative', 'Neutral', 'Positive'))

    plt.show()

    return top10

# Paper: Section 3.2
# Emotions and Programming Language

# ------------------------------------------------------------------------------
# | Language    |  Commits   |     Mean    |   Stand. Dev.     |   p-value     |
# ------------------------------------------------------------------------------

def EmotionsProgLang():
    print("Emotions and Programming Language:\n")

    projectLang = {}
    topall = []

    df = pd.read_sql_query("SELECT project_language, sentiment_com FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():
        if row['project_language'] in projectLang:
            projectLang[row['project_language']].append(float(row['sentiment_com']))
        else:
            projectLang[row['project_language']] = [float(row['sentiment_com'])]

    # print(projectLang.keys())

    for key in sorted(projectLang,  key=lambda k: len(projectLang[k]), reverse=True):

        if key:
            commits = len(projectLang[key])
            mean = stats.tmean(projectLang[key])
            std_dev = stats.tstd(projectLang[key])
            wilcoxon_test = stats.wilcoxon(projectLang[key])[1]
            # print('Wilcoxon p-value:', wilcoxon_test)    # Get p-value
            if wilcoxon_test < 0.002:
                wilcoxon_test = '< 0.002'
            # else:
            #     wilcoxon_test = wilcoxon_test[1]
            # print 'mean:', mean
            # print 'std dev:', std_dev
            # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
            topall.append([key, commits, mean, std_dev, wilcoxon_test])


    t = Texttable()
    t.add_rows([['Language', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + topall)
    print(t.draw())

    print("Emotion score average grouped by programming language.\n")

    objects = [val[0] for val in topall]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in topall]

    colors = ['orangered', 'orangered', 'orangered', 'orangered', 'orangered', 'orangered', 'orangered', 'orangered', 'skyblue', 'skyblue']
    plt.figure(figsize = (12,5))
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 3. Emotions score average grouped by programming language')

    plt.show()

    return topall

# PAPER: Part A of Section 3.3
# Emotions, Day and Time of the Week

# ------------------------------------------------------------------------------
# | Weekday    |  Commits   |     Mean    |   Stand. Dev.     |   p-value     |
# ------------------------------------------------------------------------------

def EmotionsDayofWeek():
    print("Emotions, Day of Week:\n")
    # Emotion based on day of the week: Mon - Sun
    # Emotion based on time of the day:
        # [1] Morning:      6:00 - 12:00
        # [2] Afternoon:    12:00 - 18:00
        # [3] Evening:      18:00 - 23:00
        # [4] Night:        23:00 - 6:00

    DayofWeek = {}
    weekday = []

    df = pd.read_sql_query("SELECT created_at, sentiment_com FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():

        datetime_object = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
        day = datetime_object.strftime('%A')

        if day in DayofWeek:
            DayofWeek[day].append(float(row['sentiment_com']))
        else:
            DayofWeek[day] = [float(row['sentiment_com'])]

    for key in sorted(DayofWeek,  key=lambda k: len(DayofWeek[k]), reverse=True):
        commits = len(DayofWeek[key])
        mean = stats.tmean(DayofWeek[key])
        std_dev = stats.tstd(DayofWeek[key])
        wilcoxon_test = stats.wilcoxon(DayofWeek[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
        weekday.append([key, commits, mean, std_dev, wilcoxon_test])

    t = Texttable()
    t.add_rows([['Weekday', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + weekday)
    print(t.draw())

    print('Emotion score average of commit comments grouped by weekday.\n')

    objects = [val[0] for val in weekday]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in weekday]

    colors = ['orangered', 'orangered', 'orangered', 'orangered', 'orangered', 'orangered']
    plt.figure(figsize = (12,5))    
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors, width = 0.6)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 4. Emotion score average of commi comments grouped by weekday')

    plt.show()

    return weekday

# PAPER: Part B of Section 3.3
# Emotions, Day and Time of the Week

# ---------------------------------------------------------------------------------
# | Time of Day    |  Commits   |     Mean    |   Stand. Dev.     |   p-value     |
# ---------------------------------------------------------------------------------

def EmotionsTimeofDay():
    print("Emotions, Time of Day:\n")

    TimeofDay = {}
    fourtime = []

    df = pd.read_sql_query("SELECT created_at, sentiment_com FROM commit_sentiments;", db_connection)

    for index, row in df.iterrows():

        datetime_object = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
        hour = datetime_object.strftime('%H')
        hour = int(hour)
        # print hour

        if hour >= 6 and hour < 12:
            hour_key = 'Morning'
        elif hour >= 12 and hour < 18:
            hour_key = 'Afternoon'
        elif hour >= 18 and hour < 23:
            hour_key = 'Evening'
        else:
            hour_key = 'Night'


        if hour_key in TimeofDay:
            TimeofDay[hour_key].append(float(row['sentiment_com']))
        else:
            TimeofDay[hour_key] = [float(row['sentiment_com'])]

    for key in sorted(TimeofDay,  key=lambda k: len(TimeofDay[k]), reverse=True):
        commits = len(TimeofDay[key])
        mean = stats.tmean(TimeofDay[key])
        std_dev = stats.tstd(TimeofDay[key])
        wilcoxon_test = stats.wilcoxon(TimeofDay[key])

        if wilcoxon_test[1] < 0.002:
            wilcoxon_test = '< 0.002'
        # print 'mean:', mean
        # print 'std dev:', std_dev
        # print 'Wilcoxon p-value:', wilcoxon_test    # Get p-value
        fourtime.append([key, commits, mean, std_dev, wilcoxon_test])


    t = Texttable()
    t.add_rows([['Time of Day', 'Commits:', 'Mean', 'Stand. Dev.', 'p-value']] + fourtime)
    print(t.draw())

    print('Emotion score average of commit comments grouped by time of the day.\n')

    objects = [val[0] for val in fourtime]
    y_pos = np.arange(len(objects))
    performance = [val[2] for val in fourtime]

    colors = ['skyblue', 'skyblue', 'skyblue', 'skyblue']
    plt.figure(figsize = (12,5))
    plt.bar(y_pos, performance, align='center', alpha=0.5, color=colors, width = 0.6)
    plt.xticks(y_pos, objects)
    plt.ylabel('Emotion score average')
    plt.title('Fig 5. Emotion score average of commit comments grouped by time of the day')

    plt.show()

    return fourtime

# PAPER: Section 3.4
# Emotions and Team Distribution

# This package might be helpful in mapping countries to continents
# https://pypi.org/project/incf.countryutils/

# box plot of the continent distribution

# ------------------------------------------------
# | Continents  |    Mean    |   Stand. Dev.     |
# ------------------------------------------------
