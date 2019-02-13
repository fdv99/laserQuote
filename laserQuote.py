import sqlite3

# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

conn = sqlite3.connect('laserdata.db')
c = conn.cursor()
conn.close()
carbonTable = 'Carbon_Table'
stainlessTable = 'Stainless_Table'

c.execute('CREATE TABLE carbonTable (thickness TEXT, cut_speed INTEGER, pierce_time INTEGER, cost_sq_foot REAL)')
