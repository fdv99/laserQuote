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


'''
# Variables
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

def material(materialType, materialThickness):
    sheetUnitCost = 1 #go to correct table based on materialType, and get the correct cell on materialThickness row
    cutSpeed = 10
    pierceTime = 5
    return cutSpeed, pierceTime

def laserTime(length, pierce, cutSpeed, pierceTime):
    cutTime = (length / cutSpeed) + ((pierce * pierceTime) / 60)

print(cutSpeed)

material(1, 1)

print(cutSpeed)
'''