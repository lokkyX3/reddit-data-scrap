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
                     user_agent=''
                     )

#writing retrieved list of posts into csv
def write_csv(to_csv, csv_name):
    try:
        with open(csv_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(to_csv)
            file.close()
    except Exception as e:
        print(e)

#retrieve post from reddit ~ duh
def retrieve_post(sub,post_number,csv_name):
    subreddit = reddit.subreddit(sub)
    sub_hot = subreddit.hot(limit=post_number)
    to_csv = [['title', 'score', 'comment_count', 'author', 'nsfw', 'upvote_ratio', 'post_date']]
    print('Scrapping {}...'.format(sub))
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
        write_csv(to_csv, csv_name)
    except Exception as e:
        print(e)

for sub in sub_name:
    #Note: The csv file names are saved in {subreddit name}_yyyymmdd.csv format
    csv_name = '{}_{}.csv'.format(sub,datetime.datetime.now().strftime("%Y%m%d"))
    #csv path
    csv_file = Path(csv_name)

    #check if csv file already exist to prevent overwriting before retrieving post from reddit
    if csv_file.exists():
        print('File {} already exist!'.format(csv_name))
    else:
        retrieve_post(sub,post_num,csv_name)
