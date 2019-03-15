import sys
import sqlite3
import csv
import pandas as pd
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

def loadCutDataDB():
    # This loads the cut data into the carbon table, no need to call again
    df = pd.read_csv('cutdata.csv')
    df.columns = df.columns.str.strip()
    con = sqlite3.connect('cutdata.db')
    df.to_sql("cutTable", con)
    con.close()

# loadCutDataDB()

def laserDB():
    con = sqlite3.connect('cutdata.db')

# Variables
"""
materialType = 0
materialThickness = 0
length = 0 
pierce = 0
cutSpeed = 0
pierceTime = 0
handleTime = 20
sheets = 1
engineerTime = 20
shopRate = 65
engineerRate = 85
laserRate = 105
sheetHeight = 60
sheetWidth = 120
sheetUnitCost = 0
materialCost = 0
"""


def quote():
    materialType = input("Material, c or s: ")
    if materialType == 'c':
        materialThickness = 0.120
    elif materialType == 's':
        materialThickness = 0.120
    else:
        print("Not a valid material type.")
    con = sqlite3.connect('cutdata.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM cutTable WHERE steel = ? AND type = ?', (materialThickness, materialType))
    data = cursor.fetchone()
    cutSpeed = data[3]
    pierceTime = data[4]
    sheetUnitCost = data[7]
    con.close()
    print(cutSpeed)
    print(pierceTime)
    print(sheetUnitCost)

def laserTime(length, pierce, cutSpeed, pierceTime):
    cutTime = (length / cutSpeed) + ((pierce * pierceTime) / 60)


quote()