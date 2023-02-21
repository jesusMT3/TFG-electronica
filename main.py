# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 10:03:43 2023

@author: Jesús
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from myfunctions import smooth

cols = ["No", "DateTime", "ms", "CH1", "CH2", "CH3", "CH4", "CH5", 
        "CH6", "CH7", "CH8", "CH9", "CH11", "CH12", "CH13", "CH14", 
        "CH15", "CH19", "CH20", "GS1", "GS2", "GS3", "GS4", "Alarm1", 
        "Alarm2", "Alarm3", "AlarmOut"] # columns in which the data from data is organised

def select_file():
    global df
    try:
        data = filedialog.askopenfilename()
    except FileNotFoundError:
        print('File not found')
    df = pd.read_csv(data,
                     sep="\s+|,", # two types of separation
                     names = cols, # names of the columns
                     header = None, # csv file with no header, customized "cols"
                     engine = "python",
                     skiprows = 40, # first 40 rows are datalogger specifications
                     index_col = 1) #to search for specific hours in dataframe
    print('Done')

def plot_data():
    try:
        selected = [listbox.get(idx) for idx in listbox.curselection()]
        fig, ax = plt.subplots()
        for col in selected:
            filtered_data[col] = smooth(filtered_data[col], 1000)
            filtered_data[col].plot(linewidth = 1)
        ax.legend()
        ax.set_xlabel("DateTime")
        ax.set_ylabel("Values")
        ax.set_title("Selected Data Plot")

        global canvas # add global keyword
        try:
            canvas.get_tk_widget().destroy() # remove the old plot
        except:
            pass
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def search_by():
    date = search_entry.get()
    global filtered_data
    filtered_data = df[df.index.str.startswith(date)].copy()
    filtered_data.index = filtered_data['DateTime']
    for col in filtered_data.columns:
        listbox.insert("end", col)
    return df
        
root = tk.Tk()
root.title("DataFrame Plotter")

button = tk.Button(root, text="Select file", command=select_file)
button.pack()

listbox = Listbox(root, selectmode="multiple")
listbox.pack()

search_label = tk.Label(root, text="Search by:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=search_by)
search_button.pack()

button_show = tk.Button(root, text = 'Plot data', command = plot_data)
button_show.pack()


root.mainloop()