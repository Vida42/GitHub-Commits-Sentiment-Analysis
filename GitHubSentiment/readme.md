# File Introduction

## Database manipulation File

### create.py

Connect to `vader_databse` database and create tables inside:

- `commit_sentiments`

- `commit_sentiments_store`

### manipuate_table.py

query data from `whole_database_new` database and save data into two tables we created in `vader_databse` database.


## Modeling File

### emotionStat.py

Main code of sentiment analysis. It consists of five analysis reports.

- `EmotionsProject`

get average emotion score per project, display bar chart

- `EmotionsProjectProportion`

show the proportion of positive, neutral and negative commit comments per project

- `EmotionsProgLang`

show the relationship between Emotions and Programming Language

- `EmotionsDayofWeek`

show the relationship between Emotions and Day of the Week

- `EmotionsTimeofDay`

show the relationship between Emotions and Time of one day


### gitSentiment.py

run `emotionStat.py` file


## Test File

### vader_example.py

This is a file play around with vader.

### senti_calculator.py

It's an enhanced version of `vader_example.py` to calculate sentiment.

### testone.py

This is a test file.


## Database File

### whole_database_new.db

Original database.

### vader_databse.db

Database we used in this analysis project.