import sys
import sqlite3
import csv
import pandas as pd
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

def loadStainlessDB():
    # This loads the cut data into the stainless table, no need to call again
    df = pd.read_csv('stainless_cutdata.csv')
    df.columns = df.columns.str.strip()
    con = sqlite3.connect('cutdata.db')
    df.to_sql("stainless", con)
    con.close()

def loadCarbonDB():
    # This loads the cut data into the carbon table, no need to call again
    df = pd.read_csv('carbon_cutdata.csv')
    df.columns = df.columns.str.strip()
    con = sqlite3.connect('cutdata.db')
    df.to_sql("carbon", con)
    con.close()


def laserDB():
    con = sqlite3.connect('cutdata.db')


carbonSizes = ['0.035 [20GA]', '0.047 [18GA]', '0.060 [16GA]', '0.075 [14GA]', '0.105 [12GA]', '0.120 [11GA]', '0.187 [HRPO]', '0.250 [HRPO]', '0.375 [HRPO]', '0.500 [HRPO]']
stainlessSizes = ['0.035 [20GA]', '0.047 [18GA]', '0.060 [16GA]', '0.075 [14GA]', '0.120 [11GA]', '0.187 [3/16]']
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
    materialType = input("Material, carbon or stainless:")
    if materialType == 'carbon':
        materialThickness = '0.120 [11GA]'
        # display carbonSizes list and pick size needed
    elif materialType == 'stainless':
        # display stainlessSizes list and pick size needed
        materialThickness = '0.120 [11GA]'
    else:
        print("Not a valid material type.")
    con = sqlite3.connect('cutdata.db')
    cursor = con.cursor()
    cursor.execute('SELECT CUT_SPEED FROM ? WHERE STEEL == ?', (materialType, materialThickness,))
    cutSpeed = cursor.fetchone()
    print(cutSpeed)

def laserTime(length, pierce, cutSpeed, pierceTime):
    cutTime = (length / cutSpeed) + ((pierce * pierceTime) / 60)


quote()