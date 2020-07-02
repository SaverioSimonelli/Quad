#!/usr/bin/python3

import os
import re
import qlibs

#
# Filename: fasta2text.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def fasta2text(fasta, fname):
    seqs = []
    try:
        begin = fasta.index(">")
        print(fname)
    except Exception as e:
        print(str(e))
        ename = fname[:fname.index("data") + 5] + "error.log"
        ft = open(ename, "a")
        ft.write(fname + "\n")
        ft.write(str(e) + "\n")
        ft.close()
        return seqs        
    while True:
        try:
            end = fasta[begin + 1 :].index(">") + begin
        except Exception as e:
            print(str(e))
            end = len(fasta)
        buf = fasta[begin : end]
        eol = buf.index("\n")
        text = buf[eol + 1 : ]
        text = text.replace("\n", "")
        seqs.append(text)
        begin = end + 1
        if end >= len(fasta): break
    return seqs

def save_text(seqs, regions, textdir, fname, opt):
    print(regions)
    dname = fname[fname.rindex("/") + 1: len(fname) - 6]
    print(dname)    
    if not os.path.exists(textdir + regions + "/" + dname + "/"):
        os.mkdir(textdir + regions + "/" + dname + "/")
    for i in range(len(seqs)):
        text = seqs[i]
        pos = text.find("#")
        if pos >= 0: text = text[ : pos]
        suffix = "___" + opt + "_" + str(i) + ".txt"
        
        tname = textdir + regions + "/" + dname + "/" + dname + suffix
        print(tname)
        try:
            ft = open(tname, "w")
            ft.write(text)
            ft.close()
        except: pass
    return
    

def set_text(fastadir, regions, opt):
    basedir = fastadir[:fastadir.index("Fasta")]
    textdir = basedir  + "Text/"
    qlibs.create_path(textdir + regions + "/")
    if not os.path.exists(textdir):
       os.mkdir(textdir)
    files = []
    for fname in os.listdir(fastadir):
        if fname.find(".fasta") >= 0:
            f = open(fastadir + "/" + fname, "r")
            fasta = f.read()
            f.close()
            seqs = fasta2text(fasta, fastadir + "/" + fname)
            save_text(seqs, regions, textdir, fastadir + "/" + fname, opt)
    return