#Python3
import sys, praw, psaw, json, time
from textblob import TextBlob
from datetime import datetime
from psaw import PushshiftAPI

#Command line arguments
sub_reddit = sys.argv[1]
query_name = sys.argv[2]

file_name = sys.argv[2] #file name same as query_name
extension_position = file_name.find('.json')
if(extension_position != -1):
    file_name = file_name[0:extension_position]

month = int(sys.argv[3])
day = int(sys.argv[4])
year = int(sys.argv[5])


#My client_id, client_secret, and user_agent are in my private praw.ini file
reddit = praw.Reddit('bot1')
api = PushshiftAPI(reddit)
#Date the album was announced
start_date = int(datetime(year, month, day).timestamp())

post_data = {}
post_data["posts"] = []

comment_data = {}
comment_data["comments"] = []

for entry in api.search_submissions(after=start_date, subreddit=sub_reddit, \
                                    q=query_name):
    tsent = TextBlob(entry.title)       #Title sentiment
    stsent = TextBlob(entry.selftext)   #Selftext sentiment
    if tsent.sentiment.polarity != 0            \
        or tsent.sentiment.subjectivity != 0    \
        or stsent.sentiment.polarity != 0       \
        or stsent.sentiment.subjectivity != 0:
        #If analyzer could gather anything at all, include data point
        #Technically only time and sentiment needed, but including more metadata
        new_entry = {"id" : entry.id,
                     "title" : entry.title,
                     "selftext" : entry.selftext,
                     "created_utc" : str(int(entry.created_utc)),
                     "sentiment" : str(max(tsent.sentiment.polarity,    \
                                         stsent.sentiment.polarity))
                     }
        post_data["posts"].append(new_entry)


for entry in api.search_comments(after=start_date, subreddit=sub_reddit, \
                                 q=query_name):
    bsent = TextBlob(entry.body)        #Body sentiment
    if bsent.sentiment.polarity != 0 or bsent.sentiment.subjectivity != 0:
        #If analyzer could gather anything at all, include data point
        new_entry = {"id" : entry.id,
                     "body" : entry.body,
                     "created_utc" : str(int(entry.created_utc)),
                     "sentiment" : str(bsent.sentiment.polarity)
                     }
        comment_data["comments"].append(new_entry)


with open(file_name + '_posts.json', 'w') as p:
        json.dump(post_data, p, indent=2)

with open(file_name + '_comments.json', 'w') as c:
        json.dump(comment_data, c, indent=2)
