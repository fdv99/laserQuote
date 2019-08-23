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

materialTypeLabel = tk.Label(root, text="Material Type [c,s]:", anchor="e").grid(row=1)
materialTypeEntry = tk.Entry(root)
materialTypeEntry.grid(row=1,column=1)

materialThickLabel = tk.Label(root, text="Material Thickness:", anchor="e").grid(row=2)
materialThickEntry = tk.Entry(root)
materialThickEntry.grid(row=2,column=1) 

lengthLabel = tk.Label(root, text="Cut Length:", anchor="e").grid(row=3)
lengthEntry = tk.Entry(root)
lengthEntry.grid(row=3,column=1)

pierceLabel = tk.Label(root, text="Pierces:", anchor="e").grid(row=4)
pierceEntry = tk.Entry(root)
pierceEntry.grid(row=4,column=1)

sheetLengthLabel = tk.Label(root, text="Sheet Length:", anchor="e").grid(row=5)
sheetLengthEntry = tk.Entry(root)
sheetLengthEntry.grid(row=5,column=1)

sheetWidthLabel = tk.Label(root, text="Sheet Width:", anchor="e").grid(row=6)
sheetWidthEntry = tk.Entry(root)
sheetWidthEntry.grid(row=6,column=1)

sheetNumberLabel = tk.Label(root, text="Number of sheets:", anchor="e").grid(row=7)
sheetNumberEntry = tk.Entry(root)
sheetNumberEntry.grid(row=7,column=1)

matCostLabel = tk.Label(root, text="Material Cost:", anchor="e").grid(row=9)
matCostEntry = tk.Entry(root)
matCostEntry.grid(row=9, column=1)

laserCostLabel = tk.Label(root, text="Laser Cost:", anchor="e").grid(row=10)
laserCostEntry = tk.Entry(root)
laserCostEntry.grid(row=10, column=1)

totalCostLabel = tk.Label(root, text="Total Cost:", anchor="e").grid(row=11)
totalCostEntry = tk.Entry(root)
totalCostEntry.grid(row=11, column=1)

laserRateLabel = tk.Label(root, text="Laser Rate:", anchor="e").grid(row=1, column=3)
laserRateEntry = tk.Entry(root)
laserRateEntry.grid(row=1, column=4)
laserRateEntry.insert(0, '105')

handleRateLabel = tk.Label(root, text="Handling Rate:", anchor="e").grid(row=2, column=3)
handleRateEntry = tk.Entry(root)
handleRateEntry.grid(row=2, column=4)
handleRateEntry.insert(0, '65')

handleTimeLabel = tk.Label(root, text="Handling Time:", anchor="e").grid(row=3, column=3)
handleTimeEntry = tk.Entry(root)
handleTimeEntry.grid(row=3, column=4)
handleTimeEntry.insert(0, '25')

engineerRateLabel = tk.Label(root, text="Engineering Rate:", anchor="e").grid(row=4, column=3)
engineerRateEntry = tk.Entry(root)
engineerRateEntry.grid(row=4, column=4)
engineerRateEntry.insert(0, '95')

engineerTimeLabel = tk.Label(root, text="Engineering Time:", anchor="e").grid(row=5, column=3)
engineerTimeEntry = tk.Entry(root)
engineerTimeEntry.grid(row=5, column=4)
engineerTimeEntry.insert(0, '20')

def quote():
    #Standard prices and times for laser, handling, etc..
    global laserRate 
    global handleRate 
    global handleTime 
    global sheetLength
    global sheetWidth
    global engineerRate 
    global engineerTime 
    global materialTypeEntry
    global materialThickEntry
    global lengthEntry
    global pierceEntry
    global sheetNumber
    
    materialType = materialTypeEntry.get()
    materialThickness = float(materialThickEntry.get())
    length = int(lengthEntry.get())
    pierce = int(pierceEntry.get())
    sheetLength = int(sheetLengthEntry.get())
    sheetWidth = int(sheetWidthEntry.get())
    laserRate = int(laserRateEntry.get())
    handleRate = int(handleRateEntry.get())
    handleTime = int(handleTimeEntry.get())
    engineerRate = int(engineerRateEntry.get())
    engineerTime = int(engineerTimeEntry.get())
    sheetNumber = int(sheetNumberEntry.get())
    
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
    handleCost = (((handleTime/60) * handleRate) * sheetNumber) + ((engineerTime/60) * engineerRate)
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    totalCost = laserCost + handleCost + materialCost
    print(f"Cut Time: {cutTime}")
    print(f"Laser Cost: {laserCost}")
    print(handleCost)
    print(materialCost)
    print(f"Total Cost: {totalCost}")

    
calculateBut = tk.Button(root, text="Calculate", command=quote).grid(row=8,column=1)
updateBut = tk.Button(root, text="Update", command=quote).grid(row=6,column=4)

root.mainloop()