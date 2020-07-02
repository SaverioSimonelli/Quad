#!/usr/bin/python3

import os
import dist
import qgrs
import qlibs
import graphs
import subprocess
import webbrowser
import getseq as gs
import tkinter as tk
import selectby as sb
import reverse as rev
import seqslost as sl
import config as cfgn
import fasta2text as f2t
import selectscore as sel
import qgrslengtherror as qel
import intersection as inters
from tkinter import filedialog
from tkinter import messagebox
from xml.etree import ElementTree

#
# Filename: quad.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

class Program:
    def __init__(self, root):
        self.opt = ""
        self.pop = tk.StringVar()
        self.set = tk.StringVar()
        self.upno = tk.StringVar()
        self.dwno = tk.StringVar()
        self.maxl = tk.StringVar()
        self.ming = tk.StringVar()
        self.smin = tk.StringVar()
        self.t = tk.IntVar()
        self.t.set(2) #No third column in input file
        self.threshold = tk.IntVar()
        self.r = tk.IntVar()
        self.libpath = tk.StringVar()
        cfgn.load(self)
        self.file = tk.StringVar()
        self.field = tk.StringVar()
        self.fv = tk.StringVar()
        self.s = tk.IntVar()
        self.ce = tk.IntVar()
        self.u3 = tk.IntVar()
        self.u5 = tk.IntVar()
        self.it = tk.IntVar()
        self.up = tk.IntVar()
        self.dw = tk.IntVar()
        self.err = tk.IntVar()
        self.tit = tk.StringVar()
        self.sel = tk.IntVar()
        self.root = root
        self.frame = tk.Frame(root)
        self.menubar()
    
    def menubar (self):
        root = self.root
        root.geometry("500x350")
        root.title("Quad")
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open)
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)


        seqmenu = tk.Menu(menubar, tearoff=0)
        seqmenu.add_command(label="Get Sequence", command= self.get_seq_view)
        seqmenu.add_command(label="Get Lost Sequences", command = self.lost_view)
        seqmenu.add_command(label="Reverse Complement", command= self.reverse_view)
        seqmenu.add_command(label="Quadruplexes Search", command=self.quad_search_view)
        seqmenu.add_command(label="Errors Management", command=self.errors_view)
        seqmenu.add_command(label="Quadruplexes Distribution", command=self.dist_view)
        seqmenu.add_command(label="Graphics", command=self.graphics_view)
        seqmenu.add_command(label="Selections", command=self.select_view)
        seqmenu.add_command(label="Get Intersection", command=self.intersection_view)
        menubar.add_cascade(label="Options", menu=seqmenu)
        
        confmenu = tk.Menu(menubar, tearoff=0)
        confmenu.add_command(label="Modify", command = self.config_view)
        menubar.add_cascade(label="Configuration", menu = confmenu)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Contents", command=self.contents)
        helpmenu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        return



    def get_seq_view(self):
        self.root.title("Quad - Get Sequences")
        self.opt = "get_seq"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "File: ").place(x = 30,y = 60)
        file = tk.Entry(frame, textvariable = self.file)
        file.place(x = 100,y = 60)
        tk.Button(frame, text = "Browse").place(x = 300,y = 60)
        self.root.bind('<Button-1>', self.callback)
        tk.Label(frame, text = "Sequence: ").place(x = 30,y = 90)
        self.s = tk.IntVar()
        tk.Radiobutton(frame, text = "One Fasta per Region ", variable = self.s, value = 1).place(x = 100,y = 90)
        tk.Radiobutton(frame, text = "One Fasta per Gene ", variable = self.s, value = 2).place(x = 250,y = 90)
        self.ce = tk.IntVar()
        tk.Label(frame, text = "Region: ").place(x = 30,y = 120)
        tk.Checkbutton(frame, text = "Cds Exon ", variable = self.ce).place(x = 80,y = 120)
        self.u3 = tk.IntVar()
        tk.Checkbutton(frame, text = "Utr3' Exon ", variable = self.u3).place(x = 160,y = 120)
        self.u5 = tk.IntVar()
        tk.Checkbutton(frame, text = "Utr5' Exon ", variable = self.u5).place(x = 240,y = 120)
        self.it = tk.IntVar()
        tk.Checkbutton(frame, text = "Intron ", variable = self.it).place(x = 320,y = 120)
        self.up = tk.IntVar()
        tk.Checkbutton(frame, text = "Upstream ", variable = self.up).place(x = 80,y = 150)
        upno = tk.Entry(frame, textvariable = self.upno)
        upno.place(x = 160, y = 150)
        self.dw = tk.IntVar()
        tk.Checkbutton(frame, text = "Downstream ", variable = self.dw).place(x = 240,y = 150)
        dwno = tk.Entry(frame, textvariable = self.dwno)
        dwno.place(x = 330, y = 150)
        tk.Button(frame, text = "Execute").place(x = 200,y = 180)
        self.root.bind("<Button-1>", self.callback)
        return

    def lost_view(self):
        self.root.title("Quad - Get Lost Sequences ")
        self.opt = "lost"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "Set: ").place(x = 260,y = 30)
        set = tk.Entry(frame, textvariable = self.set)
        set.place(x = 300, y = 30)
        tk.Label(frame, text = "File: ").place(x = 30,y = 60)
        file = tk.Entry(frame, textvariable = self.file)
        file.place(x = 100,y = 60)
        tk.Button(frame, text = "Browse").place(x = 300,y = 60)
        self.root.bind('<Button-1>', self.callback)
        tk.Button(frame, text = "Execute").place(x = 180,y = 150)
        self.root.bind("<Button-1>", self.callback)
        return

    def reverse_view(self):
        self.root.title("Quad - Reverse Complement")
        self.opt = "reverse"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "Set: ").place(x = 260,y = 30)
        set = tk.Entry(frame, textvariable = self.set)
        set.place(x = 360, y = 30)
        tk.Button(frame, text = "Execute").place(x = 200,y = 180)
        self.root.bind("<Button-1>", self.callback)

        return
        
    def quad_search_view(self):
        self.root.title("Quad - Quadruplexes Search")
        self.opt = "quad_search"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "Set: ").place(x = 260,y = 30)
        set = tk.Entry(frame, textvariable = self.set)
        set.place(x = 360, y = 30)
        self.rev = tk.IntVar()
        tk.Checkbutton(frame, text = "Reverse Complement", variable = self.rev).place(x = 100,y = 70)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 120)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 120)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 120)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 120)
        self.ce = tk.IntVar()
        tk.Label(frame, text = "Region: ").place(x = 30,y = 150)
        tk.Checkbutton(frame, text = "Cds Exon ", variable = self.ce).place(x = 80,y = 150)
        self.u3 = tk.IntVar()
        tk.Checkbutton(frame, text = "Utr3' Exon ", variable = self.u3).place(x = 160,y = 150)
        self.u5 = tk.IntVar()
        tk.Checkbutton(frame, text = "Utr5' Exon ", variable = self.u5).place(x = 240,y = 150)
        self.it = tk.IntVar()
        tk.Checkbutton(frame, text = "Intron ", variable = self.it).place(x = 320,y = 150)
        self.up = tk.IntVar()
        tk.Checkbutton(frame, text = "Upstream ", variable = self.up).place(x = 80,y = 180)
        self.dw = tk.IntVar()
        tk.Checkbutton(frame, text = "Downstream ", variable = self.dw).place(x = 240,y = 180)
        tk.Button(frame, text = "Execute").place(x = 200,y = 210)
        self.root.bind("<Button-1>", self.callback)
        return
    
    
    def errors_view(self):
        self.root.title("Quad - Errors Management")
        self.opt = "errors"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        self.rev = tk.IntVar()
        tk.Checkbutton(frame, text = "Reverse Complement", variable = self.rev).place(x = 100,y = 60)
        self.err = tk.IntVar()
        tk.Radiobutton(frame, text = "Split Large Files ", variable = self.err, value = 1).place(x = 30,y = 90)
        tk.Radiobutton(frame, text = "Union Splitted Files ", variable = self.err, value = 2).place(x = 150,y = 90)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 120)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 120)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 120)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 120)
        tk.Button(frame, text = "Execute").place(x = 200,y = 180)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def dist_view(self):
        self.root.title("Quad - Quadruplexes Distribution")
        self.opt = "dist"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        self.rev = tk.IntVar()
        tk.Checkbutton(frame, text = "Reverse Complement", variable = self.rev).place(x = 100,y = 60)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 90)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 90)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 90)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 90)
        tk.Button(frame, text = "Execute").place(x = 200,y = 150)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def graphics_view(self):
        self.root.title("Quad - Graphics")
        self.opt = "graph"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "Title: ").place(x = 30,y = 60)
        tit = tk.Entry(frame, textvariable = self.tit)
        tit.place(x = 100, y = 60)
        tk.Label(frame, text = "File: ").place(x = 30,y = 90)
        file = tk.Entry(frame, textvariable = self.file)
        file.place(x = 100,y = 90)
        tk.Button(frame, text = "Browse").place(x = 300,y = 90)
        self.root.bind('<Button-1>', self.callback)
        self.rev = tk.IntVar()
        tk.Checkbutton(frame, text = "Reverse Complement", variable = self.rev).place(x = 100,y = 120)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 150)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 150)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 150)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 150)
        tk.Button(frame, text = "Execute").place(x = 200,y = 180)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def select_view(self):
        self.root.title("Quad - Selections")
        self.opt = "select"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "File: ").place(x = 30,y = 60)
        file = tk.Entry(frame, textvariable = self.file)
        file.place(x = 100,y = 60)
        tk.Button(frame, text = "Browse").place(x = 300,y = 60)
        self.root.bind('<Button-1>', self.callback)
        self.sel = tk.IntVar()
        tk.Radiobutton(frame, text = "Select by: ", variable = self.sel, value = 1).place(x = 30,y = 90)
        field = tk.Entry(frame, textvariable = self.field)
        field.place(x = 110,y = 90)
        fv = tk.Entry(frame, textvariable = self.fv)
        fv.place(x = 200,y = 90)
        tk.Radiobutton(frame, text = "Select score: ", variable = self.sel, value = 2).place(x = 30,y = 120)
        self.r = tk.IntVar()
        tk.Radiobutton(frame, text = "> ", variable = self.r, value = 1).place(x=120,y=120)
        tk.Radiobutton(frame, text = "< ", variable = self.r, value = 2).place(x=150,y=120)
        tk.Radiobutton(frame, text = "= ", variable = self.r, value = 3).place(x=180,y=120)
        self.threshold = tk.IntVar()
        threshold = tk.Entry(frame, textvariable = self.threshold)
        threshold.place(x = 220,y = 120)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 150)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 150)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 150)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 150)
        tk.Button(frame, text = "Execute").place(x = 200,y = 200)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def intersection_view(self):
        self.root.title("Quad - Get Intersection")
        self.opt = "intersect"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 250, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        self.rev = tk.IntVar()
        tk.Checkbutton(frame, text = "Reverse Complement", variable = self.rev).place(x = 100,y = 60)
        self.v = tk.IntVar()
        tk.Label(frame, text = "Algorithm: ").place(x = 30,y = 90)
        tk.Radiobutton(frame, text = "QGRS Local ", variable = self.v, value = 1).place(x = 100,y = 90)
        tk.Radiobutton(frame, text = "QGRS Web ", variable = self.v, value = 2).place(x = 200,y = 90)
        tk.Radiobutton(frame, text = "PQS Finder ", variable = self.v, value = 3).place(x = 300,y = 90)
        tk.Button(frame, text = "Execute").place(x = 200,y = 150)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def config_view(self):
        self.root.title("Quad - Configuration")
        self.opt = "config"
        cfgn.load(self)
        if self.frame != None: self.frame.destroy()
        self.frame = tk.Frame(self.root, width = 450, height = 350, pady = 3)
        self.frame.grid(row = 0, columnspan = 3)
        frame = self.frame
        tk.Label(frame, text = "Population: ").place(x = 30,y = 30)
        pop = tk.Entry(frame, textvariable = self.pop)
        pop.place(x = 100, y = 30)
        tk.Label(frame, text = "Set: ").place(x = 260,y = 30)
        set = tk.Entry(frame, textvariable = self.set)
        set.place(x = 360, y = 30)
        tk.Label(frame, text = "Upstream: ").place(x = 30,y = 60)
        upno = tk.Entry(frame, textvariable = self.upno)
        upno.place(x = 100, y = 60)
        tk.Label(frame, text = "Downstream: ").place(x = 260,y = 60)
        dwno = tk.Entry(frame, textvariable = self.dwno)
        dwno.place(x = 360, y = 60)
        tk.Label(frame, text = "Qgrs: ").place(x = 130,y = 90)
        tk.Label(frame, text = "Max Length: ").place(x = 30,y = 120)
        maxl = tk.Entry(frame, textvariable = self.maxl)
        maxl.place(x = 100, y = 120)
        tk.Label(frame, text = "Min G-Group: ").place(x = 260,y = 120)
        ming = tk.Entry(frame, textvariable = self.ming)
        ming.place(x = 360, y = 120)
        tk.Label(frame, text = "Pqs: ").place(x = 130,y = 150)
        tk.Label(frame, text = "Min Score: ").place(x = 30,y = 180)
        smin = tk.Entry(frame, textvariable = self.smin)
        smin.place(x = 100, y = 180)
        tk.Label(frame, text = "Threshold: ").place(x = 30,y = 210)
        tk.Radiobutton(frame, text = "> ", variable = self.r, value = 1).place(x=100,y=210)
        tk.Radiobutton(frame, text = "< ", variable = self.r, value = 2).place(x=150,y=210)
        tk.Radiobutton(frame, text = "= ", variable = self.r, value = 3).place(x=200,y=210)
        threshold = tk.Entry(frame, textvariable = self.threshold, width = 4)
        threshold.place(x = 250, y = 210)
        tk.Label(frame, text = "Third Column: ").place(x = 30,y = 240)
        self.t = tk.IntVar()
        tk.Radiobutton(frame, text = "True ", variable = self.t, value = 1).place(x=130,y=240)
        tk.Radiobutton(frame, text = "False ", variable = self.t, value = 2).place(x=180,y=240)
        tk.Label(frame,text = "R Library Path: ").place(x = 30,y = 270)
        libpath = tk.Entry(frame, textvariable = self.libpath, width = 50)
        libpath.place(x = 150, y = 270)
        tk.Button(frame, text = "Confirm").place(x = 230,y = 300)
        self.root.bind("<Button-1>", self.callback)
        return
    
    def contents(self):
        try:
            self.root.title("Quad - Contents")
            self.opt = "content"
            cfgn.load(self)
            if self.frame != None: self.frame.destroy()
            fname = os.path.abspath(qlibs.get_docdir() + "quad.pdf")
            webbrowser.open_new_tab("file:///" + fname)
        except Exception as e:
            print(str(e))

        return
    
    def about(self):
        text = """
        Quad version 1.0
        
        Author: Saverio Simonelli
        Copyright (c) 2020 
        Licence: MIT Licence
        
        Software used:
            qgrs-cpp
            Qgrs Mapper 
            pqsfinder
            Python
            C/C++
            R
            
        Data sources:
            Genome Browser
            
        """
        messagebox.showinfo("About", text)
        return
    
    def callback(self, event):
        try:
            if event.widget.cget("text") == "Browse":
                if self.opt == "get_seq" : self.browse_get_seq()
                if self.opt == "lost" : self.browse_get_seq()
                if self.opt == "errors" : self.browse_errors()
                if self.opt == "graph" : self.browse_graphics()
                if self.opt == "select" : self.browse_select()
            if event.widget.cget("text") == "Execute":
                cfgn.save(self)
                qlibs.create_path(qlibs.get_datadir() + self.pop.get() + "/")
                if self.opt == "get_seq" : self.get_seq()
                if self.opt == "lost" : self.lost()
                if self.opt == "reverse" : self.reverse()
                if self.opt == "quad_search" : self.quad_search()
                if self.opt == "errors" : self.errors()
                if self.opt == "dist" : self.dist()
                if self.opt == "graph" : self.graphics()
                if self.opt == "select" : self.select()
                if self.opt == "intersect" : self.intersections()
                messagebox.showinfo("Quad", "END!")
            if event.widget.cget("text") == "Confirm":
                cfgn.save(self)
        except: pass
        return
    
    
    def browse_get_seq(self):
        indir = qlibs.get_inputdir()
        types = (("csv files", "*.csv"),("all files","*.*"))
        fname = filedialog.askopenfilename(parent=self.root, initialdir= indir, title='Please select a file', filetypes = types)
        self.file.set(fname)
        print("getseq")
        return
    
    def browse_errors(self):
        indir = qlibs.get_logdir() + self.pop.get() + "/"
        print(indir)
        types = (("log files", "*.log"),("all files","*.*"))
        fname = filedialog.askopenfilename(parent=self.root, initialdir= indir, title='Please select a file', filetypes = types)
        self.file.set(fname)
        return
    
    def browse_graphics(self):
        indir = qlibs.get_datadir() + self.pop.get() + "/"
        types = (("csv files", "*.csv"),("all files","*.*"))
        fname = filedialog.askopenfilename(parent=self.root, initialdir= indir, title='Please select a file', filetypes = types)
        self.file.set(fname)
        buf = fname[:fname.rfind("/")]
        buf = buf[buf.rfind("/")+ 1:]
        self.tit.set(buf)
        return
    
    def browse_select(self):
        indir = qlibs.get_datadir() + self.pop.get() + "/"
        types = (("csv files", "*.csv"),("all files","*.*"))
        fname = filedialog.askopenfilename(parent=self.root, initialdir= indir, title='Please select a file', filetypes = types)
        self.file.set(fname)
        print("select")
        return
    
    def open(self):
        indir = qlibs.get_datadir() 
        types = (("csv files", "*.csv"),("all files","*.*"))
        fname = filedialog.askopenfilename(parent=self.root, initialdir= indir, title='Please select a file', filetypes = types)
        if os.name == 'nt': os.system("start " + fname)
        if os.name == 'posix': os.system("open " + shlex.quote(fname))
        return
    
    def get_seq(self):
        #
        # Get transcript sequence from UCSC Genome Browser (https://genome.ucsc.edu/)
        #
        u = False
        d = False
        uddir = ""
        udpar = ""
        ftcidir = ""
        ftcipar = ""
        chr = ""
        nregs = 0
        regions = ""
        opts = ""
        argv = ["quad.exe"]
        argv.append(self.file.get())
        print("get")
        print(self.t)
        if int(self.up.get()) == 1: 
            argv.append("-u")
            argv.append(self.upno.get())
            u = True
            if int(self.s.get()) == 1:
                uddir = "Upstream" + str(self.upno.get()) + "OnePerRegion/"
                regions = regions + "Upstream" + str(self.upno.get())
                opts = opts + "u"
            if int(self.s.get()) == 2:
                uddir = "Upstream" +str(self.upno.get()) + "/"
                regions = regions + "Upstream" + str(self.upno.get())
                opts = opts + "u"
            if udpar == "": udpar = "Upstream" + str(self.upno.get())
            else: udpar = udpar + ";" + "Upstream" + str(self.upno.get())
        if int(self.u5.get()) == 1:  
            argv.append("-f")
            if int(self.s.get()) == 1:
                ftcidir = "UtrExon5OnePerRegion/"
                nregs = nregs + 1
                regions = regions + "UtrExon5"
                opts = opts + "f"
            if int(self.s.get()) == 2:
                ftcidir = "UtrExon5/"
                nregs = nregs + 1
                regions = regions + "UtrExon5"
                opts = opts + "f"
            if ftcipar == "": ftcipar = "UtrExon5;"
            else: ftcipar = ftcipar + "UtrExon5;"
            chr = "f"
        if int(self.u3.get()) == 1: 
            argv.append("-t")
            if int(self.s.get()) == 1:
                ftcidir = "UtrExon3OnePerRegion/"
                nregs = nregs + 1
                regions = regions + "UtrExon3"
                opts = opts + "t"
            if int(self.s.get()) == 2: 
                ftcidir = "UtrExon3/"
                nregs = nregs + 1
                regions = regions + "UtrExon3"
                opts = opts + "t"
            if ftcipar == "": ftcipar = "UtrExon3;"
            else: ftcipar = ftcipar + "UtrExon3;"
            chr = "t"
        if int(self.ce.get()) == 1:  
            argv.append("-c")
            if int(self.s.get()) == 1:
                ftcidir = "CdsExonOnePerRegion/"
                nregs = nregs + 1
                regions = regions + "CdsExon"
                opts = opts + "c"
            if int(self.s.get()) == 2: 
                ftcidir = "CdsExon/"
                nregs = nregs + 1
                regions = regions + "CdsExon"
                opts = opts + "c"
            if ftcipar == "": ftcipar = "CdsExon;"
            else: ftcipar = ftcipar + "CdsExon;"
            chr = "c"
        if int(self.it.get()) == 1:  
            argv.append("-i")
            if int(self.s.get()) == 1:
                ftcidir = "IntronOnePerRegion/"
                nregs = nregs + 1
                regions = regions + "Intron"
                opts = opts + "i"
            if int(self.s.get()) == 2:
                ftcidir = "Intron/"
                nregs = nregs + 1
                regions = regions + "Intron"
                opts = opts + "i"                
            if ftcipar == "": ftcipar = "Intron;"
            else: ftcipar = ftcipar + "Intron;"
            chr = "i"
        if int(self.dw.get()) == 1: 
            argv.append("-d")
            argv.append(self.dwno.get())
            d = True
            if int(self.s.get()) == 1: 
                uddir = "Downstream" + self.dwno.get() + "OnePerRegion/" 
                regions = regions + "Downstream" + self.dwno.get()
                opts = opts + "d"
            if int(self.s.get()) == 2: 
                uddir = "Upstream" + str(self.upno.get()) + "/" 
                regions = regions + "Downstream" + self.dwno.get()
                opts = opts + "d"
            if udpar == "": udpar = "Downstream" + self.dwno.get()
            else: udpar = udpar + ";" + "Downstream" + self.dwno.get()
        argv.append("-g")
        if int (self.s.get()) == 1:argv.append("feature")
        if int (self.s.get()) == 2:argv.append("gene")
        else: argv.append("feature")
        if self.t.get() == 1: 
            argv.append("-n") 
        print(argv)
        sets = gs.get_seq(self.pop.get(), argv)
        regionsopr = regions
        if nregs == 4 and u == True and d == True:
            regions = "FullGeneSeq"
            if int (self.s.get()) == 1:opts = "full"
            if int (self.s.get()) == 2:opts = "full_gene"
        if int (self.s.get()) == 1: 
            regionsopr = regions + "OnePerRegion"
        if int (self.s.get()) == 2: 
            regionsopr = regions 
        print (str(int (self.s.get())))
        print ("sets",sets)
        for set in sets:
            print(regionsopr)
            print("regionsopr")
            f2t.set_text(qlibs.get_datadir() + self.pop.get() + "/" + set + "/Fasta/" + regionsopr + "/", regions, opts)
        return
    
    def lost(self):
        #
        # Create a csv file  in Lost population folder, containing gene name and RNA codes  transcripts in log file from get_seq
        # 
        sl.getlost(self.file.get(), self.pop.get(), self.set.get())
        return
    
    def reverse(self):
        #
        #Create the reverse complement of each sequence in local database
        #
        rev.reverse_set(self.pop.get(), self.set.get())
        return
    
    def quad_search(self):
        #
        # Submit  sequence to a prediction algorithm
        #
        population = self.pop.get()
        set = self.set.get()
        reverse = ""
        if self.rev.get() == 1:
            #
            # Submit the reversed sequences
            #
            reverse = "ReverseComplement"
        textdir = qlibs.get_datadir()+ population + "/" + set + "/Text" + reverse + "/"
        regions = ""
        #
        # The following enable to choose region type
        #
        if int(self.up.get()) == 1: regions = regions + "Upstream" + self.upno.get() + ";"
        if int(self.u5.get()) == 1: regions = regions + "UtrExon5" + ";"
        if int(self.u3.get()) == 1: regions = regions + "UtrExon3" + ";"
        if int(self.ce.get()) == 1: regions = regions + "CdsExon" + ";"
        if int(self.it.get()) == 1: regions = regions + "Intron" + ";"
        if int(self.dw.get()) == 1: regions = regions + "Downstream" + self.dwno.get() + ";"
        if regions != "": regions = regions[: len(regions) - 1]
        algo = ""
        if int(self.v.get()) == 1: 
            #
            # Use qgrs-cpp (https://github.com/freezer333/qgrs-cpp) recompiled as library 
            #
            algo = "Qgrs" 
            qgrs.save_csv(population, textdir, regions, algo, reverse)
        if int(self.v.get()) == 2:
            #
            # Submit query to QGRS Mapper (http://bioinformatics.ramapo.edu/QGRS/analyze.php)
            #
            algo = "QgrsWeb"  
            qgrs.save_csv(population, textdir, regions, algo, reverse)
        if int(self.v.get()) == 3:
            #
            # Use pqs function from R-library pqsfinder previously installed (http://www.bioconductor.org/packages/release/bioc/html/pqsfinder.html) 
            #
            try:
                algo = "Pqs"
                script = qlibs.get_scriptsdir() + "pqs.r"
                cmd = ["Rscript", script] + [self.libpath.get(), population, textdir, regions, algo]
                result = subprocess.check_output(cmd, universal_newlines = True)
            except Exception as e:
                qlibs.trace("pqs", str(e), population)
        print("qgrs.py " + population + " " + textdir + " " + regions + " " + algo)
        return
        
    def errors(self):
        reverse = ""
        if self.rev.get() == 1: 
            #
            # Submit the reversed sequences
            #
            reverse = "ReverseComplement"
        #
        # Do you want to split large sequences which arouse dimension error in Qgrs Web, or do you want to reunite sequences already split?
        #
        if self.err.get() == 1: self.split()
        if self.err.get() == 2: self.reunion()
        return
    
    def split(self):
        #
        # Split large sequences and submit to the chosen algorithm
        #
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        reverse = ""
        if self.rev.get() == 1: reverse = "ReverseComplement"
        overlap = int(int(self.maxl.get())/2) + 1
        print(self.libpath.get())
        resp = qel.substr_not_founds(self.pop.get(), algo, overlap, reverse, nsplit=2, libpath = self.libpath.get())
        if resp == True: messagebox.showinfo("Quad", 'All sequences found.\nPlease execute "Union Splitted Files"')
        else:
            resp = messagebox.askyesno("Quad", "WARNING:\n\nSome sequences still too large\nDo you want to split again?")
            if resp == True: self.split() 
        return
    
    def reunion(self):
        #
        # Reunite split sequences
        #
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        reverse = ""
        if self.rev.get() == 1: reverse = "ReverseComplement"
        qel.save_union(self.pop.get(), algo, reverse)
        return
    
    def dist(self):
        #
        # Create a single file of GQs per set and per population
        #
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        reverse = ""
        if self.rev.get() == 1: reverse = "ReverseComplement"
        dist.dist(self.pop.get(), algo, reverse)
        return
    
    def graphics(self):
        #
        # Plot frequences per each score assigned by chosen algorithm
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        print(qlibs.get_scorename(algo))
        graphs.graph(self.pop.get(), self.file.get(), qlibs.get_scorename(algo),self.tit.get(), True)
        return
    
    def select(self):
        if self.sel.get() == 1: 
            #
            # Select a value in a column of dist-file
            #
            self.select_by()
        if self.sel.get() == 2: 
            #
            # Select by score and threshold
            #
            self.select_score()
        return
    
    def select_by(self):
        #
        # Select a value in a column of dist-file
        #
        pos = self.file.get().rfind("/")
        dir = self.file.get()[:pos + 1]
        outprefix = "selectby_" + self.fv.get() + "_" 
        outfile = self.file.get().replace(dir, dir + outprefix)
        print(outfile)
        sb.select_by(self.pop.get(), self.file.get(), outfile, self.field.get(), self.fv.get())
        return
        
    def select_score(self):
        #
        # Select by score and threshold
        #
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        if self.r.get() == 1: rel = "greater_than"
        elif self.r.get() == 2: rel = "less_than"
        elif self.r.get() == 3: rel = "equal_to"
        prefix = "selectS_" + rel + str(self.threshold.get()) + "_"
        infile = self.file.get()
        outfile = infile.replace(os.path.basename(infile), prefix + os.path.basename(infile))
        sel.select_score(self.pop.get(), infile, outfile, qlibs.get_scorename(algo), rel, self.threshold.get())
        return

    def intersections(self):
        #
        # Get common transcripts in sets of the same population from dist-file
        #
        algo = ""
        if int(self.v.get()) == 1: 
            algo = "Qgrs" 
        if int(self.v.get()) == 2:
            algo = "QgrsWeb"  
        if int(self.v.get()) == 3:
            algo = "Pqs"
        inters.intersect(self.pop.get(), algo)
        return
    
    
root = tk.Tk()
app = Program(root)
root.mainloop()