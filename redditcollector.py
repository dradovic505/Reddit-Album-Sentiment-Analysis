#Python3
import praw, psaw, json, time, redis
from textblob import TextBlob
from datetime import datetime
from psaw import PushshiftAPI

#activate python environment: $ source env/bin/activate
#install stuff and work inbetween
#deactivate python environment: $ deactivate

#my client_id, client_secret, and user_agent are in my praw.ini file
reddit = praw.Reddit('bot1')
api = PushshiftAPI(reddit)
#around the time the album was announced
start_date = int(datetime(2018, 9, 20).timestamp())

post_data = {}
post_data["posts"] = []

comment_data = {}
comment_data["comments"] = []

for entry in api.search_submissions(after=start_date, subreddit='Kanye', q='Yandhi'):
    tsent = TextBlob(entry.title)
    stsent = TextBlob(entry.selftext)
    if tsent.sentiment.polarity != 0 or tsent.sentiment.subjectivity != 0 or stsent.sentiment.polarity != 0 or stsent.sentiment.subjectivity != 0:
        #if analyzer could gather anything at all, include data point
        new_entry = {"id":entry.id,
                     "title":entry.title,
                     "selftext":entry.selftext,
                     "created_utc":str(entry.created_utc),
                     "sentiment":str(max(tsent.sentiment.polarity,stsent.sentiment.polarity))
                     }
        post_data["posts"].append(new_entry)

for entry in api.search_comments(after=start_date, subreddit='Kanye', q='Yandhi'):
    bsent = TextBlob(entry.body)
    if bsent.sentiment.polarity != 0 or bsent.sentiment.subjectivity != 0:
        new_entry = {"id":entry.id,
                     "body":entry.body,
                     "created_utc":str(entry.created_utc),
                     "sentiment":str(bsent.sentiment.polarity)
                     }
        comment_data["comments"].append(new_entry)


with open('posts.json', 'w') as yandhi:
        json.dump(comment_data, yandhi, indent=2)

with open('comments.json', 'w') as yandhi:
        json.dump(comment_data, yandhi, indent=2)
