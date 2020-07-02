#!/usr/bin/python3

import os 
import qlibs

#
# Filename: reverse.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def reverse(text):
    result = text[::-1]
    ch = "_"
    cmin = "-"
    result = result.replace("G", ch)
    result = result.replace("g", cmin)
    result = result.replace("C", "G")    
    result = result.replace("c", "g")    
    result = result.replace(ch, "C")    
    result = result.replace(cmin, "c")    
    result = result.replace("A", ch)    
    result = result.replace("a", cmin)    
    result = result.replace("T", "A")    
    result = result.replace("t", "a")    
    result = result.replace(ch, "T")    
    result = result.replace(cmin, "t")    
    return result

def reverse_file(infile, outfile):
    fin = open(infile, "r")
    buf = fin.read()
    fin.close()
    text = reverse(buf)
    fout = open(outfile, "w")
    fout.write(text)
    fout.close()
    return

def reverse_set(population, set):
    datadir = qlibs.get_datadir()
    indir = datadir + population + "/" + set + "/Text/"
    outdir = indir.replace("/Text/", "/TextReverseComplement/")
    regions = []
    for r, d, f in os.walk(indir):
        for rname in d:
            regions.append(rname)
    for region in regions:
        for r, d, f in os.walk(indir + region):
            for gene_code in d:
                for r, d, f in os.walk(indir + region  + "/" + gene_code + "/"):
                    for fname in f:
                        infile = indir + region  + "/" + gene_code + "/" + fname
                        outfile = outdir + region + "/" + gene_code + "/" + fname
                        qlibs.create_path(outdir + region + "/" + gene_code + "/")
                        qlibs.trace("reverse", infile, population)
                        reverse_file(infile, outfile)
    return 
