#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from xml.etree import ElementTree

#
# Filename: config.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def save(self):
    tree = ElementTree.ElementTree(file = "quad.xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "population":
            child.text = self.pop.get()
        if child.tag == "set":
            child.text = self.set.get()
        if child.tag == "upstream": 
            child.text = self.upno.get()                
        if child.tag == "downstream":
            child.text = self.dwno.get()
        if child.tag == "maxlength":
            child.text = self.maxl.get()
        if child.tag == "minggroup":
            child.text = self.ming.get()
        if child.tag == "minscore":
            child.text = self.smin.get()
        if child.tag == "thirdcolumn":
            #child.text = self.t
            if self.t.get() == 1: child.text = "True"
            elif self.t.get() == 2: child.text = "False"
        if child.tag == "threshold": child.text = str(self.threshold.get())
        if child.tag == "relation": 
            if self.r.get() == 1: child.text = "greater_than"
            elif self.r.get() == 2: child.text = "less_than"
            elif self.r.get() == 3: child.text = "equal_to"
        if child.tag == "rlibrarypath": 
            child.text = self.libpath.get()
    tree.write("quad.xml")
    return


def load(self):
    tree = ElementTree.ElementTree(file = "quad.xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "population":
            if child.text != None: self.pop.set(child.text)
        if child.tag == "set":
            if child.text != None: self.set.set(child.text)
        if child.tag == "upstream": 
            if child.text != None: self.upno.set(child.text)
        if child.tag == "downstream":
            if child.text != None: self.dwno.set(child.text)
        if child.tag == "maxlength":
            if child.text != None: self.maxl.set(child.text)
        if child.tag == "minggroup":
            if child.text != None: self.ming.set(child.text)
        if child.tag == "minscore":
            if child.text != None: self.smin.set(child.text)
        if child.tag == "thirdcolumn":
            if child.text.lower() == "true": self.t.set(1)# = "True"
            if child.text.lower() == "false": self.t.set(2) #= "False"
        if child.tag == "threshold":
            if child.text != None: self.threshold.set(child.text)
        if child.tag == "relation":
            if child.text.lower() == "greater_than": self.r.set(1)
            if child.text.lower() == "less_than":self.r.set(2)
            if child.text.lower() == "equal_to":self.r.set(3)
        if child.tag == "rlibrarypath": 
            if child.text != None: self.libpath.set(child.text)
        print(child.tag, child.text)
    return




def show(app):
    root = tk.Toplevel(app.root)
    frame = Config(root)
    frame.load(app)
    root.mainloop()