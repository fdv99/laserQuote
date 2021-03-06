import sys
import sqlite3
import csv
import pandas as pd
import tkinter as tk
import datetime
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

root = tk.Tk()
topFrame = tk.Frame(root)
topFrame.pack()
bottomFrame = tk.Frame(root)
bottomFrame.pack(side = "left")
rightFrame = tk.Frame(root)
rightFrame.pack(side="right")
root.title("V6 Laser Quote")

def loadCutDataDB():
    # This loads the cut data into the carbon table, no need to call again
    df = pd.read_csv('cutdata.csv')
    df.columns = df.columns.str.strip()
    con = sqlite3.connect('cutdata.db')
    df.to_sql("cutTable", con)
    con.close()
#loadCutDataDB()

def loadQuoteDataDB():
    # This creates the quote data table, no need to call again
    df = pd.read_csv('quotedata.csv')
    df.columns = df.columns.str.strip()
    con = sqlite3.connect('quotedata.db')
    df.to_sql("quoteTable", con)
    con.close()
#loadQuoteDataDB()

def laserDB():
    con = sqlite3.connect('cutdata.db')

def quote():
    global totalCost
    materialType = matVariable.get()
    materialThickness = float(thickVariable.get())
    length = int(lengthEntry.get())
    pierce = int(pierceEntry.get())
    sheetLength = int(sheetLengthEntry.get())
    sheetWidth = int(sheetWidthEntry.get())
    formingTime = float(formTimeEntry.get())
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
    handleCost = (((handleTime / 60) * handleRate) * sheetNumber) + ((engineerTime / 60) * engineerRate) + ((formingTime / 60) * handleRate)
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    materialCost = str(round(materialCost, 2))
    matCostEntry.insert(0, materialCost)
    totalCost = float(laserCost) + float(handleCost) + float(materialCost)
    totalCost = str(round(totalCost, 2))
    totalCostEntry.insert(0, totalCost)

def saveQuote():
    customer = custVariable.get()
    jobNumber = jobNumEntry.get()
    currentDate = datetime.date.today()
    conQ = sqlite3.connect('quotedata.db')
    cursorQ = conQ.cursor()
    cursorQ.execute('INSERT INTO quoteTable(Customer, PO, Date, Material_Cost, Total_Cost) VALUES(?,?,?,?,?)', (customer, jobNumber, currentDate, materialCost, totalCost))
    conQ.close()

material = ["Carbon", "Stainless"]
matVariable = tk.StringVar(root)
matVariable.set(material[0])
materialTypeLabel = tk.Label(topFrame, text="Material Type:").grid(row=1)
materialTypeOption = tk.OptionMenu(topFrame, matVariable, *material)
materialTypeOption.grid(row=1,column=1)

thickness = ["0.035", "0.047", "0.060", "0.075", "0.105", "0.120", "0.187", "0.250", "0.375", "0.500"]
thickVariable = tk.StringVar(root)
thickVariable.set(thickness[5])
materialThickLabel = tk.Label(topFrame, text="Material Thickness:").grid(row=2)
materialThickOption = tk.OptionMenu(topFrame, thickVariable, *thickness)
materialThickOption.grid(row=2, column=1)

customerList = ['AMS Automation', 'Innovative Machinery', 'PMI2', 'Technico']
custVariable = tk.StringVar(root)
custVariable.set(customerList[0])
customerLabel = tk.Label(topFrame, text="Customer:").grid(row=3)
customerOption = tk.OptionMenu(topFrame,custVariable, *customerList)
customerOption.grid(row=3,column=1)

jobNumLabel = tk.Label(topFrame, text="PO/Job Number:").grid(row=4)
jobNumEntry = tk.Entry(topFrame)
jobNumEntry.grid(row=4,column=1)

lengthLabel = tk.Label(topFrame, text="Cut Length:").grid(row=5)
lengthEntry = tk.Entry(topFrame)
lengthEntry.grid(row=5,column=1)

pierceLabel = tk.Label(topFrame, text="Pierces:").grid(row=6)
pierceEntry = tk.Entry(topFrame)
pierceEntry.grid(row=6,column=1)

sheetLengthLabel = tk.Label(topFrame, text="Sheet Length [in]:").grid(row=7)
sheetLengthEntry = tk.Entry(topFrame)
sheetLengthEntry.grid(row=7,column=1)

sheetWidthLabel = tk.Label(topFrame, text="Sheet Width [in]:").grid(row=8)
sheetWidthEntry = tk.Entry(topFrame)
sheetWidthEntry.grid(row=8,column=1)

formTimeLabel = tk.Label(topFrame, text="Forming Time [min]:").grid(row=9)
formTimeEntry = tk.Entry(topFrame)
formTimeEntry.grid(row=9,column=1)

sheetNumberLabel = tk.Label(topFrame, text="Number of sheets:").grid(row=10)
sheetNumberEntry = tk.Entry(topFrame)
sheetNumberEntry.grid(row=10,column=1)

#Calculated Entries for costs and time:
cutTimeLabel = tk.Label(bottomFrame, text="Cutting Time:").grid(row=0)
cutTimeEntry = tk.Entry(bottomFrame)
cutTimeEntry.grid(row=0,column=1)

matCostLabel = tk.Label(bottomFrame, text="Material Cost:").grid(row=1)
matCostEntry = tk.Entry(bottomFrame)
matCostEntry.grid(row=1, column=1)

laserCostLabel = tk.Label(bottomFrame, text="Laser Cost:").grid(row=2)
laserCostEntry = tk.Entry(bottomFrame)
laserCostEntry.grid(row=2, column=1)

totalCost = 0
totalCostLabel = tk.Label(bottomFrame, text="Total Cost:").grid(row=3)
totalCostEntry = tk.Entry(bottomFrame)
totalCostEntry.grid(row=3, column=1)

#Default values for shop rates that can be changed:
laserRateLabel = tk.Label(rightFrame, text="Laser Rate:").grid(row=1, column=3)
laserRateEntry = tk.Entry(rightFrame)
laserRateEntry.grid(row=1, column=4)
laserRateEntry.insert(0, '105')

handleRateLabel = tk.Label(rightFrame, text="Handling Rate:").grid(row=2, column=3)
handleRateEntry = tk.Entry(rightFrame)
handleRateEntry.grid(row=2, column=4)
handleRateEntry.insert(0, '65')

handleTimeLabel = tk.Label(rightFrame, text="Handling Time:").grid(row=3, column=3)
handleTimeEntry = tk.Entry(rightFrame)
handleTimeEntry.grid(row=3, column=4)
handleTimeEntry.insert(0, '25')

engineerRateLabel = tk.Label(rightFrame, text="Engineering Rate:").grid(row=4, column=3)
engineerRateEntry = tk.Entry(rightFrame)
engineerRateEntry.grid(row=4, column=4)
engineerRateEntry.insert(0, '90')

engineerTimeLabel = tk.Label(rightFrame, text="Engineering Time:").grid(row=5, column=3)
engineerTimeEntry = tk.Entry(rightFrame)
engineerTimeEntry.grid(row=5, column=4)
engineerTimeEntry.insert(0, '20')

#Buttons  
calculateBut = tk.Button(topFrame, text="Calculate", command=quote).grid(row=11,column=1)

updateBut = tk.Button(rightFrame, text="Update", command=quote).grid(row=6,column=4)

root.mainloop()