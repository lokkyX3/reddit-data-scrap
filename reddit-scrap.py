import praw
import datetime
import csv
import os
from pathlib import Path

#subreddit name list
sub_name = ['news','all']

#number of post to retrieve
post_num = 10

#OAuth credentials from reddit account
reddit = praw.Reddit(
                     client_id='',
                     client_secret='',
                     username='',
                     password='',
                     user_agent='',
                     )

#writing retrieved list of posts into csv
def write_csv(to_csv, sub):
    try:
        with open(sub+'_'+datetime.datetime.now().strftime('%Y%m%d')+'.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(to_csv)
            file.close()
    except Exception as e:
        print(e)

#retrieve post from reddit ~ duh
def retrieve_post(sub,post_number):
    subreddit = reddit.subreddit(sub)
    sub_hot = subreddit.hot(limit=post_number)
    to_csv = [['title', 'score', 'comment_count', 'author', 'nsfw', 'upvote_ratio', 'post_date']]
    print('Scrapping '+sub+'...')
    try:
        for post in sub_hot:
            if not post.stickied:
                retrieved = [
                            post.title,
                            post.score,
                            post.num_comments,
                            post.author.name,
                            post.over_18,
                            post.upvote_ratio,
                            datetime.datetime.fromtimestamp(post.created).strftime('%Y-%m-%d %H:%M')
                            ]
                to_csv.append(retrieved)
        write_csv(to_csv, sub)
    except Exception as e:
        print(e)

for sub in sub_name:
    #csv path
    csv_file = Path(sub+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.csv') #Note: The csv file names are saved in {subreddit name}_yyyymmdd.csv format

    #check if csv file already exist to prevent overwriting before retrieving post from reddit
    if csv_file.exists():
        print('File '+sub+'_'+datetime.datetime.now().strftime("%Y%m%d")+'.csv already exist')
    else:
        retrieve_post(sub,post_num)
