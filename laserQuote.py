import sys
import sqlite3
import csv
import pandas as pd
import tkinter as tk
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

root = tk.Tk()
root.title("V6 Laser Quote")
label = tk.Label(root, text = "Quote for Laser Cutting").grid(row=0,column=0)
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

materialTypeLabel = tk.Label(root, text="Material Type [c,s]:").grid(row=1)
materialTypeEntry = tk.Entry(root)
materialTypeEntry.grid(row=1,column=1)

materialThickLabel = tk.Label(root, text="Material Thickness:").grid(row=2)
materialThickEntry = tk.Entry(root)
materialThickEntry.grid(row=2,column=1) 

lengthLabel = tk.Label(root, text="Cut Length:").grid(row=3)
lengthEntry = tk.Entry(root)
lengthEntry.grid(row=3,column=1)

pierceLabel = tk.Label(root, text="Pierces:").grid(row=4)
pierceEntry = tk.Entry(root)
pierceEntry.grid(row=4,column=1)

def quote():
    #Standard prices and times for laser, handling, etc..
    laserRate = 105
    handleRate = 65
    handleTime = 30
    sheetLength = 120
    sheetWidth = 60
    engineerRate = 90
    engineerTime = 20
    global materialTypeEntry
    global materialThickEntry
    global lengthEntry
    global pierceEntry
    #These do not work as the entries are outside of the function
    materialType = materialTypeEntry.get()
    materialThickness = float(materialThickEntry.get())
    length = int(lengthEntry.get())
    pierce = int(pierceEntry.get())


    #This section does not work right, don't understand why right now.
    '''materialType = input("Material, c or s: ").strip()
    if materialType == 'c' or 's':
        materialThickness = 0.187
    else:
        print('Not a valid Material type!')

    length = int(input("Enter the length of cut: "))
    pierce = int(input("Enter the number of pierces: "))'''
    
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
    handleCost = ((handleTime/60) * handleRate) + ((engineerTime/60) * engineerRate)
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    totalCost = laserCost + handleCost + materialCost
    print(f"Cut Time: {cutTime}")
    print(f"Laser Cost: {laserCost}")
    print(handleCost)
    print(materialCost)
    print(f"Total Cost: {totalCost}")



# Error because the get is inside quote function    
calculateBut = tk.Button(root, text="Calculate", command=quote).grid(row=5,column=1)



root.mainloop()