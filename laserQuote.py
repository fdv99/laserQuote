import sys
import sqlite3
import csv
import pandas as pd
import tkinter as tk
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

root = tk.Tk()
root.title("V6 Laser Quote")
label = tk.Label(root, text = "Quote for Laser Cutting").pack()
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
    #Standard prices and times for laser, handling, etc..
    laserRate = 105
    handleRate = 65
    handleTime = 30
    sheetLength = 120
    sheetWidth = 60

    materialType = input("Material, c or s: ")
    if materialType != 'c' or 's':
        print('Not a valid Material type!')
        materialType = input("Material, c or s: ")
    materialThickness = 0.187

    length = int(input("Enter the length of cut: "))
    pierce = int(input("Enter the number of pierces: "))
    
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
    cutTime = (length / cutSpeed) + ((pierce * pierceTime) / 60)
    laserCost = (cutTime/60) * laserRate
    handleCost = (handleTime/60) * handleRate
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    totalCost = laserCost + handleCost + materialCost
    print(cutTime)
    print(laserCost)
    print(handleCost)
    print(materialCost)
    print(totalCost)

quote()
root.mainloop()