#sqlite choice database
import sqlite3
#data is in json format
import json
#datetime for logging ::optional
from datetime import datetime
#timeframe value is year-month of data 
#You could also make this a list of these, then iterate over them if you like.
#For now, I will just work with the May 2015 file.
timeframe = ['2015-05']
#to build a transaction of items to be commited at once to save resourses
sql_transaction = []
#With SQLite, the database is created with the connect if it doesn't already exist.
connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

#planning to store a few values of data
def create_table():
    def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")

#main code block
if __name__ == '__main__':
    create_table()
    row_counter = 0
    paired_rows = 0

    with open('J:/chatdata/reddit_data/{}/RC_{}'.format(timeframe.split('-')[0],timeframe), buffering=1000) as f:
        for row in f: