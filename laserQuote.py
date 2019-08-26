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

def quote():
    global totalCost
    materialType = materialTypeEntry.get()
    materialThickness = float(thickVariable.get())
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
    
    totalCostEntry.delete(0, 'end')
    matCostEntry.delete(0, 'end')
    laserCostEntry.delete(0, 'end')

    con = sqlite3.connect('cutdata.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM cutTable WHERE steel = ? AND type = ?', (materialThickness, materialType))
    data = cursor.fetchone()
    cutSpeed = data[3]
    pierceTime = data[4]
    sheetUnitCost = data[7]
    con.close()
    cutTime = (length / cutSpeed) + ((pierce * pierceTime) / 60)
    laserCost = (cutTime/60) * laserRate
    laserCost = str(round(laserCost, 2))
    laserCostEntry.insert(0, laserCost)
    handleCost = (((handleTime/60) * handleRate) * sheetNumber) + ((engineerTime/60) * engineerRate)
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    materialCost = str(round(materialCost, 2))
    matCostEntry.insert(0, materialCost)
    totalCost = float(laserCost) + float(handleCost) + float(materialCost)
    totalCost = str(round(totalCost, 2))
    totalCostEntry.insert(0, totalCost)
    print(f"Cut Time: {cutTime}")
    print(f"Laser Cost: {laserCost}")
    print(f"Total Cost: {totalCost}")


materialTypeLabel = tk.Label(root, text="Material Type [c,s]:", anchor="e").grid(row=1)
materialTypeEntry = tk.Entry(root)
materialTypeEntry.grid(row=1,column=1)

thickness = ["0.035", "0.047", "0.060", "0.075", "0.105", "0.120", "0.187", "0.250", "0.375", "0.500"]
thickVariable = tk.StringVar(root)
thickVariable.set(thickness[5])
materialThickLabel = tk.Label(root, text="Material Thickness:", anchor="e").grid(row=2)
materialThickOption = tk.OptionMenu(root, thickVariable, *thickness)
materialThickOption.grid(row=2, column=1)

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

formTimeLabel = tk.Label(root, text="Forming Time:", anchor="e").grid(row=7)
formTimeEntry = tk.Entry(root)
formTimeEntry.grid(row=7,column=1)

sheetNumberLabel = tk.Label(root, text="Number of sheets:", anchor="e").grid(row=8)
sheetNumberEntry = tk.Entry(root)
sheetNumberEntry.grid(row=8,column=1)

#Calculated Entries for costs and time:
cutTimeLabel = tk.Label(root, text="Cutting Time:", anchor="e").grid(row=10)
cutTimeEntry = tk.Entry(root)
cutTimeEntry.grid(row=10,column=1)

matCostLabel = tk.Label(root, text="Material Cost:", anchor="e").grid(row=11)
matCostEntry = tk.Entry(root)
matCostEntry.grid(row=11, column=1)

laserCostLabel = tk.Label(root, text="Laser Cost:", anchor="e").grid(row=12)
laserCostEntry = tk.Entry(root)
laserCostEntry.grid(row=12, column=1)

totalCost = 0
totalCostLabel = tk.Label(root, text="Total Cost:", anchor="e").grid(row=13)
totalCostEntry = tk.Entry(root)
totalCostEntry.grid(row=13, column=1)

#Default values for shop rates that can be changed:
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
  
calculateBut = tk.Button(root, text="Calculate", command=quote).grid(row=9,column=1)

updateBut = tk.Button(root, text="Update", command=quote).grid(row=6,column=4)

root.mainloop()