# Subreddit Sentiment Analysis

Provided a subreddit, query word, and date (month day year), redditcollector.py will search that subreddit for all posts and comments that contain the query from the date provided to the current date. The posts and comments are all run through a sentiment analyzer and given a score from -1.0 to 1.0. That score, along with metadata and the actual post or comment, are placed in json files [query]_posts.json and [query]_comments.json .

Example:

    python3 redditcollector.py [subreddit name] [query word] [month] [day] [year]


Provided a subreddit and the query word, graphing.py takes the .json files
and graphs the average sentiment of posts and comments by week, from the start date to the current date.

Example:

    python3 graphing.py [subreddit name] [query word]
