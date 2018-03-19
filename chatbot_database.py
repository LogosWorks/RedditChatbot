import sqlite3
import json
from datetime import datetime

timeframe = '2006-01'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")

def format_data(data):
	data = data.replace('\n',' newlinechar ').replace('\r',' newlinechar ').replace('"',"'")
	return data

def find_parent(pid):
	try:
		sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
		c.execute(sql)
		result = c.fetchone()
		if result != None:
			return result[0]
		else: return False
	except Exception as e:
		#print(str(e))
		return False

def find_existing_score(pid):
	try:
		sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
		c.execute(sql)
		result = c.fetchone()
		if result != None:
			return result[0]
		else: return False
	except Exception as e:
		#print(str(e))
		return False

def acceptable(data):
	#Acceptability Constants
	MAX_WORDS = 50 #one future alg requires under 50 words
	MIN_WORDS = 0 #may 'better' train output
	MAX_CHARS = 1000 #speed dial
	MIN_CHARS = 1 #may 'better' train output

	if len(data.split()) > MAX_WORDS:
		return False
	elif len(data.split()) < MIN_WORDS:
		return False
	elif len(data) > MAX_CHARS:
		return False
	elif len(data) < MIN_CHARS:
		return False
	elif data == '[deleted]':
		return False
	elif data == '[removed]':
		return False
	else:
		return True

def transaction_bldr():
	MAX_TRANSACTION = 1000
	global sql_transaction
	sql_transaction.append(sql)
	if len(sql_transaction) > MAX_TRANSACTION:
		c.execute('BEGIN TRANSACTION')
		for s in sql_transaction:
			try:
				c.execute(s)
			except Exception as e:
				raise e
		connection.commit()
		sql_transaction = []

def sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
	try:
		sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
		transaction_bldr(sql)
	except Exception as e:
		print('s0 insertion', str(e))

def sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
	try:
		sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
		transaction_bldr(sql)
	except Exception as e:
		print('s0 insertion', str(e))

def sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score):
	try:
		sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
		transaction_bldr(sql)
	except Exception as e:
		raise e

if __name__ == '__main__':
	create_table()
	row_counter = 0
	paired_rows = 0

	with open('/Users/thomasedgerton/Repos/RedditChatbot/data/{}/RC_{}'.format(timeframe.split('-')[0],timeframe), buffering=1000) as f:
		for row in f:
			print(row)
			row_counter += 1
			row = json.loads(row)
			parent_id = row['parent_id']
			body = format_data(row['body'])
			created_utc = row['created_utc']
			score = row['score']
			subreddit = row['subreddit']
			comment_id = row['name']
			parent_data = find_parent(parent_id)
			# maybe check for a child, if child, is our new score superior? If so, replace. If not...

			if score >= 2:
				existing_comment_score = find_existing_score(parent_id)
				if existing_comment_score:
					if score > existing_comment_score:
						if acceptable(body):
							sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
				else:
					if acceptable(body):
						if parent_data:
							sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
							paired_rows += 1
						else:
							sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
			if row_counter % 1000 == 0:
				print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))


















