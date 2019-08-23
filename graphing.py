import json, time, pprint, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from datetime import datetime
#dont use pylab, use pyplot
#important dates
#09/17/2018, 09/29/2018, 11/23/2018


with open('posts.json') as p:
    json_data_posts = json.load(p)

with open('comments.json') as c:
    json_data_comments = json.load(c)

def sortFirst(val):
    return val[0]

# print(json_data['posts'][0]['title'])

dates_posts = []
for post in json_data_posts['posts']:
    dates_posts.append((int(post['created_utc']), float(post['sentiment'])))

dates_comments = []
for comment in json_data_comments['comments']:
    dates_comments.append((int(comment['created_utc']), float(comment['sentiment'])))

dates_posts.sort(key=sortFirst, reverse=False)
dates_comments.sort(key=sortFirst, reverse=False)
bar_time = []   #x-axis
bar_sentiment = []  #y-axis
time_posts = []
sentiment_posts = []
time_comments = []
sentiment_comments = []

def populate_bar(time_type, sentiment_type, arr):
    start_index = 0
    for i in range(len(arr)):
        start_interval_date = datetime.utcfromtimestamp(arr[start_index][0]).date()
        current_date = datetime.utcfromtimestamp(arr[i][0]).date()
        difference = current_date - start_interval_date
        if difference.days > 6:
            interval = []
            for j in range(start_index,i):
                interval.append(arr[j][1])

            time_type.append(str(start_interval_date))
            interval_sentiment = np.average(interval)
            sentiment_type.append(interval_sentiment)
            start_index = i

populate_bar(time_posts, sentiment_posts, dates_posts)
populate_bar(time_comments, sentiment_comments, dates_comments)

# print(len(time_posts))
# print(len(time_comments))

for date in time_posts:
    bar_time.append(date)

for i in range(len(sentiment_posts)):
    bar_sentiment.append((sentiment_posts[i]+sentiment_comments[i])/2)

y_pos = np.arange(len(bar_time))
bar = plt.bar(y_pos, bar_sentiment, align='center', alpha=0.5)

plt.title('Yandhi sentiment on r/Kanye over time')
plt.xlabel('Dates of posts & comments')
plt.ylabel('Sentiment (-1.0 to 1.0)')
# plt.xticks([0,10,20,30], ['a', 'b', 'c', 'd'])
plt.xticks(range(0,len(bar_time),9), bar_time[0:len(bar_time):9])
plt.tick_params(axis='x',which='both',bottom=True,top=False,labelbottom=True, labelrotation=15)

plt.show()
