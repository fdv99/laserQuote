import tkinter as tk

root = tk.Tk()
topFrame = tk.Frame(root, height=200, width=200, bg="grey")
topFrame.grid(row=0,column=0)
bottomFrame = tk.Frame(root, height=200, width=200, bg="red")
bottomFrame.grid(row=1,column=0)
rightFrame = tk.Frame(root, height=400, width=200, bg="orange")
rightFrame.grid(row=0,column=1)
root.title("V6 Laser Quote")

root.mainloop()