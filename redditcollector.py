#Python3
import praw, psaw, json, time
from datetime import datetime
from psaw import PushshiftAPI

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
    new_entry = {"id":entry.id,
                 "title":entry.title,
                 "selftext":entry.selftext,
                 "created_utc":str(entry.created_utc)
                 }
    post_data["posts"].append(new_entry)

for entry in api.search_comments(after=start_date, subreddit='Kanye', q='Yandhi'):
    new_entry = {"id":entry.id,
                 "body":entry.body,
                 "created_utc":str(entry.created_utc)
                 }
    comment_data["comments"].append(new_entry)


with open('posts.json', 'w') as yandhi:
        json.dump(comment_data, yandhi, indent=2)

with open('comments.json', 'w') as yandhi:
        json.dump(comment_data, yandhi, indent=2)
