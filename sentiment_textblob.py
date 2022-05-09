import pandas as pd
from matplotlib import dates as mdate
from matplotlib import ticker
from datetime import datetime as dt
from TweetStore import TweetStore
from TweetStore import TweetStore
import preprocessor as p
from textblob import TextBlob
from matplotlib import pyplot as plt
import csv
import time

def piechart(positive, neutral, negative, title):#set the pie chart
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['green', 'blue', 'red']
    explode = (0.1, 0, 0)
    plt.pie([positive, neutral, negative], labels=labels, explode=explode, colors=colors, shadow=True,
            autopct='%1.1f%%')
    plt.title(title)

def sentiment_pie(data, title): #analysis the tweet and plot the result
    neg = 0
    pos = 0
    neu = 0
    results = []
    for row in data:
        cleaned_text = p.clean(row[2])
        sentiment = TextBlob(cleaned_text).sentiment

        new_row = row
        if sentiment.subjectivity > 0.1:
            if sentiment.polarity > 0:
                pos += 1
                new_row.append('positive')
            elif sentiment.polarity == 0:
                neu += 1
                new_row.append('neutral')
            else:
                neg += 1
                new_row.append('negative')
        results.append(new_row)
    piechart(pos, neu, neg, title)

def read_csv_file(file_name, date_index): #Read csv file
                                          #param file_name: csv file name
                                          #return: information in csv file
    with open(file_name, encoding='utf8')as f:
        f_csv = csv.reader(f)
        data = []
        data1 = []
        for row in f_csv:
            data.append(row)
    index = data.pop(0)
    data2 = sorted(data, key=lambda x: x[date_index])
    data1.append(row[1])
    return data2

def read_txt(txtfile):
    # Read txt file and return texts
    file = open(txtfile, 'r', encoding='utf8')
    lines = file.readlines()
    df = []
    x = ''
    for line in lines:
        if line != '\n':
            x += line.replace('\n', ' ')
        else:
            df.append(x)
            x = ''
    return df

plt.rcParams['font.size'] = 10  #Set the font size for all plots
test_df = read_csv_file('influencerM1Tweets.csv', 2)
df_text = []
for i in test_df:
    df_text.append(i[2])
fig = plt.figure()
time1 = time.perf_counter()
sentiment_pie(test_df, 'TextBlob')
time2 = time.perf_counter()
plt.show()
run_time = time2 - time1
print('Run time using TextBlob: ', run_time)