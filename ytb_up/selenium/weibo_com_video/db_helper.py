
import sqlite3
import time

DB_NAME = 'weibo_database'

def db_create_db():
    conn = sqlite3.connect(DB_NAME) 
    c = conn.cursor()
    conn.execute('''
          CREATE TABLE IF NOT EXISTS videos
          (id INTEGER PRIMARY KEY,video_id TEXT UNIQUE,comments_time INTEGER )
          ''')

    conn.commit()
    

def db_update_status(video_id):
    comments_time = time.time()
    conn = sqlite3.connect(DB_NAME) 
    
    conn.execute("insert into videos(video_id,comments_time) values('{}',{})".format(video_id,comments_time) )
    conn.commit()
    

def db_is_video_already_commented(video_id):
    conn = sqlite3.connect(DB_NAME) 
    cursor = conn.execute("SELECT * FROM videos where video_id='{}'".format(video_id))
    result = cursor.fetchone()
    if result is None:
        return False
    return True

def db_clear_db():
    conn = sqlite3.connect(DB_NAME) 
    one_m = time.time() - 3600*24 * 30
    cursor = conn.execute("DELETE FROM videos where comments_time<{}".format(one_m))
    conn.commit()


