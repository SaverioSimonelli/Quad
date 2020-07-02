#!/usr/bin/python3

import qlibs
import subprocess
import numpy as np
import matplotlib.pyplot as plt

#
# Filename: graphs.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def get_scores(population, datafile, nscore):
    rows = qlibs.get_rows(datafile)
    header = False
    result = []
    ncol = -1
    for row in rows:
        cols = row.split(";")
        if len(cols) > 1: 
            if header == False:
                ncol = qlibs.find(nscore, cols)
                if  ncol >= 0: header = True
                else:
                    ncol = qlibs.find(nscore.replace('"',''), cols)
                    if  ncol >= 0: header = True
            else:
                if cols[ncol].isnumeric() == True: result.append(int(cols[ncol]))
                else: qlibs.trace("graph_freq", datafile + "\n" + str(cols), population)
    return result
    
def get_fields(population, datafile, xname, yname):
    rows = qlibs.get_rows(datafile)
    header = False
    x = []
    y = []
    ncol = -1
    for row in rows:
        cols = row.split(";")
        if len(cols) > 1: 
            if header == False:
                xcol = qlibs.find(xname, cols)
                if  xcol >= 0: header = True
                ycol = qlibs.find(yname, cols)
                if  ycol >= 0: header = True
            else:
                if cols[xcol].replace(",","").replace("-","").isdecimal() == True: x.append(float(cols[xcol].replace(",",".")))
                else: 
                    x.append(0)
                    qlibs.trace("graph_fields" + xname, datafile + "\n" + str(cols), population)
                if cols[ycol].replace(",","").replace("-","").isdecimal() == True: y.append(float(cols[ycol].replace(",",".")))
                else:
                    y.append(0)
                    qlibs.trace("graph_fields" + yname, datafile + "\n" + str(cols), population)
    return [x, y]
    
    
def freqs(list):
    minel = min(list)
    maxel = max(list)
    data = []
    freq = []
    for i in range(minel, maxel + 1):
        data.append(i)
        freq.append(list.count(i))
    return [data, freq]
    
def select(population, datafile, xname, yname, title, show = False):
    data = get_fields(population, datafile, xname, yname)
    if len(data) == 0: return
    print(len(data), len(data[0]),len(data[1]))
    plt.figure()
    plt.plot(data[0],data[1],'ro')
    plt.title(title)
    plt.ylabel(yname)
    plt.xlabel(xname)
    drawname = datafile.replace(".csv",".png")
    plt.savefig(drawname)
    if show == True: plt.show()
    return

def draw_genes_exp(population, datafile, xname, yname, title, show = False):
    data = get_genes(population, datafile, xname, yname)
    if len(data) == 0: return
    print(len(data), len(data[0]),len(data[1]))
    plt.figure()
    plt.plot(data[0],data[1],'ro')
    plt.title(title)
    plt.ylabel(yname)
    plt.xlabel(xname)
    drawname = datafile.replace(".csv",".png")
    plt.savefig(drawname)
    if show == True: plt.show()
    return

def get_genes(population, datafile, xname, yname):
    rows = qlibs.get_rows(datafile)
    header = False
    x = []
    y = []
    xcol = -1
    ycol = -1
    prev = ""
    id = 0
    for row in rows:
        cols = row.split(";")
        if len(cols) > 1: 
            if header == False:
                xcol = qlibs.find(xname, cols)
                if  xcol >= 0: header = True
                ycol = qlibs.find(yname, cols)
                if  ycol >= 0: header = True
            else:
                if cols[xcol] != prev: 
                    id = id + 1
                    prev = cols[xcol]                    
                x.append(id)
                if cols[ycol].replace(",","").replace("-","").isdecimal() == True: y.append(float(cols[ycol].replace(",",".")))
                else:
                    y.append(0)
                    qlibs.trace("graph_fields" + yname, datafile + "\n" + str(cols), population)
    return [x, y]


def graph(population, datafile, nscore, title, show = False):
    try:
        scores = get_scores(population, datafile, nscore)
        print(scores)
        if len(scores) == 0: return
        minscore = min(scores)
        maxscore = max(scores)
        ascores = np.array(scores)
        mean = round(np.mean(ascores),3)
        median = np.median(ascores)
        std = round(np.std(ascores),3)
        values = ":  min = " + str(minscore) + "  max = " + str(maxscore) + "  mean = " + str(mean) + "  median = " + str(median) + "  std = " + str(std)
        tab = freqs(scores)
        print(tab)
        plt.figure()
        plt.plot(tab[0],tab[1])
        plt.title(title)
        plt.ylabel("Frequencies")
        plt.xlabel(nscore + values)
        drawname = datafile.replace(".csv",".png")
        plt.savefig(drawname)
        if show == True: plt.show()
    except Exception as e:
        print(str(e))
    return


