import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()


def creating_sessions_table(): # func for making our session table
    cursor.execute(
        """CREATE TABLE sessions (session_id char(128) UNIQUE NOT NULL ,atime timestamp NOT NULL default current_timestamp
         ,data text) """)
    print 'session table has created'


def creating_usersdata_table(): # func for making our userdata table
    cursor.execute("""CREATE TABLE userdata( id integer PRIMARY KEY ,
    username text unique ,password text,email text)
    """)
    print "usersdata table has created"


# creating_sessions_table()
# creating_usersdata_table()
