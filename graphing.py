#Python3
import sys, json, time, pprint, math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from datetime import datetime

#Command line arguments
sub_reddit = sys.argv[1]

file_name = sys.argv[2]
extension_position = file_name.find('.json')
if(extension_position != -1):
    file_name = file_name[:extension_position]

with open(file_name + '_posts.json') as p:
    json_data_posts = json.load(p)

with open(file_name + '_comments.json') as c:
    json_data_comments = json.load(c)

def sortFirst(val):
    return val[0]

#Add the time and sentiment values of posts to an array
posts = []
for post in json_data_posts['posts']:
    posts.append((int(post['created_utc']), float(post['sentiment'])))

#add the time and sentiment values of comments to an array
comments = []
for comment in json_data_comments['comments']:
    comments.append((int(comment['created_utc']),  \
                           float(comment['sentiment'])))

#Sort by ascending date
posts.sort(key=sortFirst, reverse=False)
comments.sort(key=sortFirst, reverse=False)

bar_date = []           #x-axis
bar_sentiment = []      #y-axis
#Temporary arrays before they are averaged
post_sentiment = []
comment_dates = []
comment_sentiment = []

#Convert time from UTC to a date, then if the array entry is within the
    #current week,
def populate_bar(date, sentiment, arr):

    start_index = 0
    for i in range(len(arr)):
        start_date = datetime.utcfromtimestamp(arr[start_index][0]).date()
        current_date = datetime.utcfromtimestamp(arr[i][0]).date()
        difference = current_date - start_date
        if difference.days > 6:
            interval = []
            #Place all values within a week as a single interval entry
            for j in range(start_index, i):
                interval.append(arr[j][1])

            #date is the same for all the data points within that week
            date.append(str(start_date))
            #sentiment must be averaged amongst all posts/comments
            avg_sentiment = np.average(interval)
            sentiment.append(avg_sentiment)
            start_index = i


populate_bar(bar_date, post_sentiment, posts)
populate_bar(comment_dates, comment_sentiment, comments)

for i in range(len(post_sentiment)):
    bar_sentiment.append((post_sentiment[i] + comment_sentiment[i]) / 2)

y_pos = np.arange(len(bar_date))
bar = plt.bar(y_pos, bar_sentiment, align='center', alpha=0.5, color="purple")

plt.title(file_name + ' sentiment on r/' + sub_reddit +     \
          ' (1 bar = average sentiment in a week)')
plt.xlabel('Dates of posts & comments')
plt.ylabel('Sentiment (-1.0 to 1.0)')
plt.xticks(range(0, len(bar_date), 5), bar_date[0:len(bar_date):5])
plt.tick_params(axis='x', which='both', bottom=True, top=False,    \
                labelbottom=True, labelrotation=15)

plt.show()
