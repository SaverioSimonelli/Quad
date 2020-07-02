#!/usr/bin/python3

import os
import datetime

#
# Filename: qlibs.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def create_dir(basedir):
	dirs =["Upstream5000", "Utr5Exon", "CdsExon", "Utr3Exon", "Intron", "Downstream5000", "FullGeneSeq"]
	if not os.path.exists(basedir):
		os.mkdir(basedir)
	basedir = basedir + "/Text/"
	if not os.path.exists(basedir):
		os.mkdir(basedir)
	for d in dirs:
		if not os.path.exists(basedir + d + "/"):
			os.mkdir(basedir + d + "/")

def create_path(path):
    newpath = ""
    buf = path
    while buf.find("/") >= 0:
        newpath = newpath + buf[: buf.find("/")] + "/"
        if buf.find("/") >= 0: buf = buf[buf.find("/") + 1:]
        else: buf = ""
        if not os.path.exists(newpath):
            os.mkdir(newpath)
    return


def get_rows(file):
    fin = open(file, "r")
    buf = fin.read()
    fin.close()
    rows = buf.split("\n")
    return rows


def trace(prefix, text, pop = "5ConditionsAnalysis"):
    logdir = get_logdir() 
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logdir = logdir +  pop + "/"
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    ename = logdir + prefix + "_error" + str(datetime.date.today()).replace("-","") + ".log"
    ft = open(ename, "a")
    ft.write(text + "\n")
    ft.close()
    

def get_datadir():
    datadir = "./data/"
    if not os.path.exists(datadir):
        datadir = "../data/"
        if not os.path.exists(datadir):
            datadir = "../../data/"
    return datadir

def get_docdir():
    docdir = "./doc/"
    if not os.path.exists(docdir):
        docdir = "../doc/"
        if not os.path.exists(docdir):
            docdir = "../../doc/"
    return docdir

def get_logdir():
    logdir = "./log/"
    if not os.path.exists(logdir):
        logdir = "../log/"
        if not os.path.exists(logdir):
            logdir = "../../log/"
    return logdir

def get_inputdir():
    inputdir = "./inputData/"
    if not os.path.exists(inputdir):
        inputdir = "../inputData/"
        if not os.path.exists(inputdir):
            inputdir = "../../inputData/"
    return inputdir
    
def get_scriptsdir():
    dir = "./scripts/"
    if not os.path.exists(dir):
        dir = "../scripts/"
        if not os.path.exists(dir):
            dir = "../../scripts/"
    return dir

def find(elem, list):
    for i in range(len(list)):
        if list[i] == elem: return i
    return -1

def get_uniques(infile, ncol = 0):
    fin = open(infile, "r")
    buf = fin.read()
    fin.close()
    rows = buf.split("\n")
    result = []
    for row in rows:
        cols = row.split(";")
        if len(cols) > ncol:
            if find(cols[ncol], result) < 0 and cols[ncol] != "": result.append(cols[ncol])
    return result

def get_uniquerows(file, population):
    fin = open(file, "r")
    buf = fin.read()
    fin.close()
    data = ""
    while buf.find("\n") >= 0:
        row = buf[: buf.find("\n")]
        if buf.find("\n") < len(buf): buf = buf[buf.find("\n") + 1 :]
        else: buf = ""
        if buf.find(row) < 0: data = data + row + "\n"
        else: 
            trace("urows", file, population)
            trace("urows", row, population)
            
        
    return data

def get_scorename(algo):
    nscore = ""
    if algo == "Qgrs": nscore = "GS"
    if algo == "QgrsWeb": nscore = "G-Score"
    if algo == "Pqs": nscore = '"score"'
    return nscore