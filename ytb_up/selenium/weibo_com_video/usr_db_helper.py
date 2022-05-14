
import sqlite3


def db_create_db():
    conn = sqlite3.connect('wb_usr_database') 
    c = conn.cursor()
    conn.execute('''
          CREATE TABLE IF NOT EXISTS users
          (id INTEGER PRIMARY KEY,user_id TEXT UNIQUE)
          ''')
    conn.execute('''
          CREATE TABLE IF NOT EXISTS status
          (user_id TEXT)
          ''')
    conn.commit()
    

def db_update_status(row_id):
    conn = sqlite3.connect('wb_usr_database') 
    conn.execute('DELETE FROM status WHERE 1' )
    conn.execute('insert into status values({})'.format(row_id) )
    conn.commit()
    

def db_get_status():
    conn = sqlite3.connect('wb_usr_database') 
    cursor = conn.execute("SELECT * FROM status")
    result = cursor.fetchone()
    if result is None:
        return 0
    return result[0]


def db_get_usr_count():
    conn = sqlite3.connect('wb_usr_database') 
    cursor = conn.execute('select * from users;')
    return len(cursor.fetchall())

def db_get_last_usr():
    conn = sqlite3.connect('wb_usr_database') 
    cursor = conn.execute("SELECT * FROM users ORDER BY rowid DESC LIMIT 1")
    result = cursor.fetchone()
    return result[0]

def db_add_usr(usr):
    try:
        conn = sqlite3.connect('wb_usr_database') 
        conn.execute('insert into users(user_id) values ({})'.format(usr) )
        conn.commit()
    except:
        print('Failed to insert:' + usr)


def db_get_usr_list(rowid):
    conn = sqlite3.connect('wb_usr_database') 
    cursor = conn.execute("SELECT * FROM users where rowid > {} ORDER BY rowid ASC LIMIT 5".format(rowid))
    result = cursor.fetchall()
    return result