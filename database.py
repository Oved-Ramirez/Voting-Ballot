import sqlite3


def create_table():
    con = sqlite3.connect("Ballotdata.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ballot (First_name TEXT, Last_name TEXT, NUID TEXT, Vote TEXT)')
    con.commit()
    con.close()