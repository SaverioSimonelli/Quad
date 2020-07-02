#!/usr/bin/python3

import os
import qlibs
import datetime

#
# Filename: intersection.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def intersect(population, algo):
    lists = []
    sets = [] 
    dists = []
    indir = qlibs.get_datadir() + population + "/"
    outfile = indir + "intersect_genes_" + population + str(datetime.date.today()).replace("-","") + ".csv"
    for set in os.listdir(indir):
        if os.path.isdir(indir + set):
            files = [f for f in os.listdir(indir + set) if os.path.isfile(indir + set + "/" + f)]
            lastfile = ""
            for file in files:
                try:
                    if file.index("dist_" + algo) == 0 and file.index(".csv") == len(file) - 4:
                        if file > lastfile: lastfile = file
                except: pass
            if lastfile == "": qlibs.trace("intersect", set, pop = population)
            else:
                lists.append(qlibs.get_uniques(indir + set + "/" + lastfile))
                sets.append(set)
                f = open(indir + set + "/" + lastfile, "r")
                buf = f.read()
                f.close()
                dists.append(buf)
    elems = []
    setreps = []
    setidxs = []
    for i in range(len(sets) - 1):
        j = i + 1
        while j < len(lists):
            for elem in lists[i]:
                if qlibs.find(elem, lists[j]) >= 0:
                    k = qlibs.find(elem, elems)
                    if k >= 0:
                        if qlibs.find(sets[j], setreps[k]) < 0:
                            setreps[k].append(sets[j])
                            setidxs[k].append(j)
                    else: 
                        elems.append(elem)
                        list = [sets[i],sets[j]]
                        setreps.append(list)
                        list = [i, j]
                        setidxs.append(list)
            j = j + 1
    text = ""
    print(sets)
    print(setreps)
    print(setidxs)
    for i in range(len(elems)):
        text = text + elems[i] + ";"
        for set in setreps[i]: text = text + set + ";" 
        text = text + "\n"  
    if text == "": text = "No intersection found"
    fout = open(outfile, "w")
    fout.write(text)
    fout.close()
    
    text = ""
    for i in range(len(elems)):
        j = setidxs[i][0]
        buf = dists[j]
        print(j)
        print(elems[i])
        rows = buf.split("\n")
        for row in rows:
            if row.find(elems[i]) >= 0: 
                text = text + row 
                for set in setreps[i]: text = text + set + ";" 
                text = text + "\n" 
    outfile = indir + "intersect_dists_" + algo + "_" + population + str(datetime.date.today()).replace("-","") + ".csv"
    fout = open(outfile, "w")
    fout.write(text)
    fout.close()
    
    return
    