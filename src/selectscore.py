#!/usr/bin/python3

import os
import qlibs


#
# Filename: selectscore.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def select_score(population, infile, outfile, nval, rel, threshold):
    print(infile)
    rows = qlibs.get_rows(infile)
    header = 1000
    text = ""
    posgs = -1
    for i in range(len(rows)):
        cols = rows[i].split(";")
        if len(cols) > 1:
            if header == 1000:
                text = rows[i] + ("\n")
                header = i
                hcols = rows[i].split(";")
                posgs = qlibs.find(nval, hcols)
                if posgs == -1:
                    posgs = qlibs.find(nval.replace('"',''), hcols)
                    if posgs == -1:
                        qlibs.trace("selectS", infile, population)
                        return
            if i > header:
                if rel == "greater_than":
                    if int(cols[posgs]) >= threshold: text = text + rows[i] + "\n"
                if rel == "less_than":
                    if int(cols[posgs]) <= threshold: text = text + rows[i] + "\n"
                if rel == "equal_to":
                    if int(cols[posgs]) == threshold: text = text + rows[i] + "\n"
    fout = open(outfile, "w")
    fout.write(text)
    fout.close()
    return 
