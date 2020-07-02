#!/usr/bin/python3

import os
import qlibs 

#
# Filename: selectby.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def select_by(population, infile, outfile, nval, val):
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
                        qlibs.trace("selectBy", infile, population)
                        return
            if i > header:
                if cols[posgs] == val: text = text + rows[i] + "\n"
    fout = open(outfile, "w")
    fout.write(text)
    fout.close()
    return 
