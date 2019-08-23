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

sheetWidthLabel = tk.Label(root, text="Sheet Length:", anchor="e").grid(row=6)
sheetWidthEntry = tk.Entry(root)
sheetWidthEntry.grid(row=6,column=1)

matCostLabel = tk.Label(root, text="Material Cost:", anchor="e").grid(row=8)
matCostEntry = tk.Entry(root)
matCostEntry.grid(row=8, column=1)

laserCostLabel = tk.Label(root, text="Laser Cost:", anchor="e").grid(row=9)
laserCostEntry = tk.Entry(root)
laserCostEntry.grid(row=9, column=1)

totalCostLabel = tk.Label(root, text="Total Cost:", anchor="e").grid(row=10)
totalCostEntry = tk.Entry(root)
totalCostEntry.grid(row=10, column=1)

laserRateLabel = tk.Label(root, text="Laser Rate:", anchor="e").grid(row=1, column=3)
laserRateEntry = tk.Entry(root)
laserRateEntry.grid(row=1, column=4)

handleRateLabel = tk.Label(root, text="Handling Rate:", anchor="e").grid(row=2, column=3)
handleRateEntry = tk.Entry(root)
handleRateEntry.grid(row=2, column=4)

handleTimeLabel = tk.Label(root, text="Handling Time:", anchor="e").grid(row=3, column=3)
handleTimeEntry = tk.Entry(root)
handleTimeEntry.grid(row=3, column=4)

engineerRateLabel = tk.Label(root, text="Engineering Rate:", anchor="e").grid(row=4, column=3)
engineerRateEntry = tk.Entry(root)
engineerRateEntry.grid(row=4, column=4)

engineerTimeLabel = tk.Label(root, text="Engineering Time:", anchor="e").grid(row=5, column=3)
engineerTimeEntry = tk.Entry(root)
engineerTimeEntry.grid(row=5, column=4)

def quote():
    #Standard prices and times for laser, handling, etc..
    global laserRate = 105
    global handleRate = 65
    global handleTime = 30
    global sheetLength
    global sheetWidth
    global engineerRate = 90
    global engineerTime = 20
    global materialTypeEntry
    global materialThickEntry
    global lengthEntry
    global pierceEntry
    
    materialType = materialTypeEntry.get()
    materialThickness = float(materialThickEntry.get())
    length = int(lengthEntry.get())
    pierce = int(pierceEntry.get())
    sheetLength = int(sheetLengthEntry.get())
    sheetWidth = int(sheetWidthEntry.get())
    
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
calculateBut = tk.Button(root, text="Calculate", command=quote).grid(row=7,column=1)
updateBut = tk.Button(root, text="Update", command=quote).grid(row=6,column=4)



root.mainloop()