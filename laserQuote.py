import sys
import sqlite3
import csv
import pandas as pd
import tkinter as tk
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

root = tk.Tk()
topFrame = tk.Frame(root)
topFrame.pack()
bottomFrame = tk.Frame(root)
bottomFrame.pack(side = "bottom")
rightFrame = tk.Frame(root)
rightFrame.pack(side ="right", fill="y")
root.title("V6 Laser Quote")

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


materialTypeLabel = tk.Label(topFrame, text="Material Type [c,s]:", anchor="e").grid(row=1)
materialTypeEntry = tk.Entry(topFrame)
materialTypeEntry.grid(row=1,column=1)

thickness = ["0.035", "0.047", "0.060", "0.075", "0.105", "0.120", "0.187", "0.250", "0.375", "0.500"]
thickVariable = tk.StringVar(root)
thickVariable.set(thickness[5])
materialThickLabel = tk.Label(topFrame, text="Material Thickness:", anchor="e").grid(row=2)
materialThickOption = tk.OptionMenu(topFrame, thickVariable, *thickness)
materialThickOption.grid(row=2, column=1)

lengthLabel = tk.Label(topFrame, text="Cut Length:", anchor="e").grid(row=3)
lengthEntry = tk.Entry(topFrame)
lengthEntry.grid(row=3,column=1)

pierceLabel = tk.Label(topFrame, text="Pierces:", anchor="e").grid(row=4)
pierceEntry = tk.Entry(topFrame)
pierceEntry.grid(row=4,column=1)

sheetLengthLabel = tk.Label(topFrame, text="Sheet Length:", anchor="e").grid(row=5)
sheetLengthEntry = tk.Entry(topFrame)
sheetLengthEntry.grid(row=5,column=1)

sheetWidthLabel = tk.Label(topFrame, text="Sheet Width:", anchor="e").grid(row=6)
sheetWidthEntry = tk.Entry(topFrame)
sheetWidthEntry.grid(row=6,column=1)

formTimeLabel = tk.Label(topFrame, text="Forming Time:", anchor="e").grid(row=7)
formTimeEntry = tk.Entry(topFrame)
formTimeEntry.grid(row=7,column=1)

sheetNumberLabel = tk.Label(topFrame, text="Number of sheets:", anchor="e").grid(row=8)
sheetNumberEntry = tk.Entry(topFrame)
sheetNumberEntry.grid(row=8,column=1)

#Calculated Entries for costs and time:
cutTimeLabel = tk.Label(bottomFrame, text="Cutting Time:", anchor="e").grid(row=0)
cutTimeEntry = tk.Entry(bottomFrame)
cutTimeEntry.grid(row=0,column=1)

matCostLabel = tk.Label(bottomFrame, text="Material Cost:", anchor="e").grid(row=1)
matCostEntry = tk.Entry(bottomFrame)
matCostEntry.grid(row=1, column=1)

laserCostLabel = tk.Label(bottomFrame, text="Laser Cost:", anchor="e").grid(row=2)
laserCostEntry = tk.Entry(bottomFrame)
laserCostEntry.grid(row=2, column=1)

totalCost = 0
totalCostLabel = tk.Label(bottomFrame, text="Total Cost:", anchor="e").grid(row=3)
totalCostEntry = tk.Entry(bottomFrame)
totalCostEntry.grid(row=3, column=1)

#Default values for shop rates that can be changed:
laserRateLabel = tk.Label(rightFrame, text="Laser Rate:", anchor="e").grid(row=1, column=3)
laserRateEntry = tk.Entry(rightFrame)
laserRateEntry.grid(row=1, column=4)
laserRateEntry.insert(0, '105')

handleRateLabel = tk.Label(rightFrame, text="Handling Rate:", anchor="e").grid(row=2, column=3)
handleRateEntry = tk.Entry(rightFrame)
handleRateEntry.grid(row=2, column=4)
handleRateEntry.insert(0, '65')

handleTimeLabel = tk.Label(rightFrame, text="Handling Time:", anchor="e").grid(row=3, column=3)
handleTimeEntry = tk.Entry(rightFrame)
handleTimeEntry.grid(row=3, column=4)
handleTimeEntry.insert(0, '25')

engineerRateLabel = tk.Label(rightFrame, text="Engineering Rate:", anchor="e").grid(row=4, column=3)
engineerRateEntry = tk.Entry(rightFrame)
engineerRateEntry.grid(row=4, column=4)
engineerRateEntry.insert(0, '95')

engineerTimeLabel = tk.Label(rightFrame, text="Engineering Time:", anchor="e").grid(row=5, column=3)
engineerTimeEntry = tk.Entry(rightFrame)
engineerTimeEntry.grid(row=5, column=4)
engineerTimeEntry.insert(0, '20')
  
calculateBut = tk.Button(topFrame, text="Calculate", command=quote).grid(row=9,column=1)

updateBut = tk.Button(rightFrame, text="Update", command=quote).grid(row=6,column=4)

root.mainloop()