import sys
import sqlite3
import csv
import pandas as pd
import tkinter as tk
# This program will replace my excel spreadsheet of the same purpose, storing quotes in a database or an excel file

root = tk.Tk()
root.title("V6 Laser Quote")
label = tk.Label(root, text = "Quote for Laser Cutting").grid(row=0,column=0)

def quote():
    #Standard prices and times for laser, handling, etc..
    laserRate = 105
    handleRate = 65
    handleTime = 30
    sheetLength = 120
    sheetWidth = 60
    engineerRate = 90
    engineerTime = 20
    materialType = 'c'
    materialThickness = 0.120
    length = 0
    pierce = 0

    materialTypeLabel = tk.Label(root, text="Material Type [c,s]:").grid(row=1)
    materialTypeEntry = tk.Entry(root).grid(row=1,column=1)

    materialThickLabel = tk.Label(root, text="Material Thickness:").grid(row=2)
    materialThickEntry = tk.Entry(root).grid(row=2,column=1)
        
    lengthLabel = tk.Label(root, text="Cut Length:").grid(row=3)
    lengthEntry = tk.Entry(root).grid(row=3,column=1)

    pierceLabel = tk.Label(root, text="Pierces:").grid(row=4)
    pierceEntry = tk.Entry(root).grid(row=4,column=1)

    def getValues(materialType, materialThickness, length, pierce):
        materialType = materialTypeEntry.get()
        materialThickness = materialThickEntry.get()
        length = lengthEntry.get()
        pierce = pierceEntry.get()
        return materialType, materialThickness, length, pierce

    calculateBut = tk.Button(root, text="Calculate", command= lambda: getValues(materialType, materialThickness, length, pierce)).grid(row=5,column=1)
 
     
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
    handleCost = ((handleTime/60) * handleRate) + ((engineerTime/60) * engineerRate)
    materialCost = ((sheetLength * sheetWidth) / 144) * sheetUnitCost
    totalCost = laserCost + handleCost + materialCost
    print(f"Cut Time: {cutTime}")
    print(f"Laser Cost: {laserCost}")
    print(handleCost)
    print(materialCost)
    print(f"Total Cost: {totalCost}")

    


quote()
root.mainloop()