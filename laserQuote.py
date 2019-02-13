import sqlite3

# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

conn = sqlite3.connect('laserdata.db')
c = conn.cursor()

carbonTable = """
CREATE TABLE CarbonTable (
    thickness TEXT,
    cut_speed INTEGER,
    pierce_time INTEGER,
    cost_sq_foot REAL)"""

stainlessTable = """
CREATE TABLE StainlessTable (
    thickness TEXT,
    cut_speed INTEGER,
    pierce_time INTEGER,
    cost_sq_foot REAL)"""
try:
    c.execute(carbonTable)
    c.execute(stainlessTable)
except:
    print('Table already exists')
