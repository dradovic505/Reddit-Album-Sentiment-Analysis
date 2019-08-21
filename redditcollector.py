#Python3
import praw

reddit = praw.Reddit(client_id='my_id',
                     client_secret='my_secret',
                     user_agent='my_agent')

print(reddit.read_only)

subreddit = reddit.subreddit('Kanye')

for submission in subreddit.hot(limit=10):
    print(submission.title)
