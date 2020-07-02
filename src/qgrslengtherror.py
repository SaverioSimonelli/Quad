#!/usr/bin/python3

from ctypes import *
import os
import qgrs
import qlibs
from xml.etree import ElementTree
from itertools import combinations

#
# Filename: qgrslengtherror.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def get_filecount(population, algo):
    logdir = qlibs.get_logdir() + population + "/"
    files = []
    for name in os.listdir(logdir):
        if os.path.isfile(os.path.join(logdir, name)):
            if name.find(algo.lower() + "_split_") >= 0:
                if name.find(".log") >= 0:
                    files.append(name)
    count = len(files)
    return count

def get_filename (population, algo, count):
    logdir = qlibs.get_logdir() + population + "/"
    fname = logdir + algo.lower() + "_split_" + str(count) + ".log"
    return fname

def start_file(population, algo):
    logdir = qlibs.get_logdir() + population + "/"
    startf = get_filename(population, algo, 0)
    files = []
    for name in os.listdir(logdir):
        if os.path.isfile(os.path.join(logdir, name)):
            if name.find(algo.lower() + "_error") >= 0:
                if name.find(".log") >= 0:
                    files.append(name)
    list = []
    for file in files:
        infile = logdir + file
        f = open(infile, "r")
        buf = f.read()
        f.close()
        lines = buf.split("\n")
        for line in lines:
            if line.find("C:/") >= 0 or line.find("./") >= 0:
                if line.find(".txt") >= 0:
                    if qlibs.find(line, list) <0:
                        list.append(line)
    f = open(startf, "w")
    for line in list:
        f.write(line + "\n")
    f.close()
        
    return
    

def split_string(string, nsplit, overlap):
    first_length = round(len(string) / int(nsplit))
    #print(first_length + overlap)
    first_half = string[0:first_length + overlap]
    second_half = string[first_length - overlap:]
    return [first_half , second_half]


def split_file(population, algo, infile, outdir, nsplit, overlap, reverse):
    fin = open(infile, "r")
    buf = fin.read()
    fin.close()
    splits = split_string(buf, nsplit, overlap)
    text = ""
    splitf = []
    for i in range(len(splits)):
        splitf.append(outdir + infile[infile.rfind("/") + 1 : len(infile) - 4] + "_split_" + str(i) + ".txt")
        
    for i in range(len(splitf)):
        fout = open (splitf[i], "w")
        fout.write(splits[i])
        fout.close()
        splittedoutfile = splitf[i].replace("/Text" + reverse + algo + "Splitted", "/" + algo +  reverse + "Splitted").replace(".txt", ".csv")
        buf = splittedoutfile[splittedoutfile.find(algo  + reverse +  "Splitted") :]
        length = buf.find("/") + 2
        splittedoutdir = splittedoutfile[:splittedoutfile.find("/" + algo + reverse + "Splitted") + length]
        #print (splittedoutfile)
        if not os.path.exists(splittedoutdir):
            os.mkdir(splittedoutdir)
        if not os.path.exists(splittedoutfile):
            if algo == "QgrsWeb": qgrs.qgrs_web(population, splitf[i], splittedoutfile)
            if algo == "Qgrs":
                if platform.system().find("Windows") >= 0: libcpp = cdll.LoadLibrary("../lib/Qgrs.dll")
                if platform.system().find("Linux") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-linux.a")
                if platform.system().find("Darwin") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-mac.so")
                qgrs.qgrs_local(population, splitf[i], splittedoutfile, libcpp)
            if algo == "Pqs": qgrs.pqs(population, splitf[i], splittedoutfile)
        else:
            print(splittedoutfile)
            print("ex")

def load():
    tree = ElementTree.ElementTree(file = "quad.xml")
    root = tree.getroot()
    upno = ""
    dwno = ""
    for child in root:
        if child.tag == "upstream": 
            if child.text != None: upno = child.text
        if child.tag == "downstream":
            if child.text != None: dwno = child.text
    return [upno, dwno]

def split_dir(infile):
    [upno, dwno] = load()
    
    filename = infile[ : infile.find("_split_") ]
    gene_code = filename[ : filename.find("___")]
    buf = filename[filename.find("___") + 3: ]
    bbuf = buf.split("_")
    r = bbuf[0]
    region = ""
    rr = ["u","f","t","c","i","d"]
    regions = ["Upstream" + upno, "UtrExon5", "UtrExon3", "CdsExon", "Intron", "Downstream" + dwno]
    l = len(r)
    rrr = list(combinations (rr, l))
    combs = list(combinations (regions, l))
    for i in range(len(rrr)):
        rbuf= ""
        cbuf = ""
        for j in range(l):
            rbuf = rbuf + rrr[i][j]
            cbuf = cbuf + combs[i][j]
        if r == rbuf: region = cbuf
    print (region)
    print (gene_code)
    return [filename, gene_code, region]

def union(indir, set, dir, infile, population, algo, reverse):
    fgr = split_dir(infile)
    name = fgr[0]
    csvudir = indir + set + "/" 
    if not os.path.exists(csvudir):
        os.mkdir(csvudir)
    csvudir = indir + set + "/" + algo + reverse + "/" 
    if not os.path.exists(csvudir):
        os.mkdir(csvudir)
    csvudir = indir + set + "/" + algo  + reverse +  "/" + fgr[2] + "/" 
    if not os.path.exists(csvudir):
        os.mkdir(csvudir)
    csvudir = indir + set + "/" + algo  + reverse +  "/" + fgr[2] + "/" + fgr[1] + "/"
    if not os.path.exists(csvudir):
        os.mkdir(csvudir)
    if name.find(".csv") < 0: csvufile = csvudir + name + ".csv" 

    ucsvdir = indir + "/" + set + "/" 
    if not os.path.exists(ucsvdir):
        os.mkdir(ucsvdir)
    ucsvdir = indir + "/" + set + "/" + algo  + reverse + "Union/" 
    if not os.path.exists(ucsvdir):
        os.mkdir(ucsvdir)
    ucsvdir = indir + "/" + set + "/" + algo  + reverse +  "Union/" + fgr[2] + "/" 
    if not os.path.exists(ucsvdir):
        os.mkdir(ucsvdir)
    ucsvdir = indir + "/" + set + "/" + algo  + reverse +  "Union/" + fgr[2] + "/" + fgr[1] + "/"
    if not os.path.exists(ucsvdir):
        os.mkdir(ucsvdir)
    if name.find(".csv") < 0: ucsvfile = ucsvdir + name + ".csv"
    
    split_files = []
    split_texts = []
    split_dirs = []
    if not os.path.exists(csvufile):
        if os.path.sdir(indir + "/" + set + "/"):
            for bufdir in os.listdir(indir + "/" + set + "/"):
                if bufdir.find(algo + reverse + "Splitted") >= 0:
                    if os.path.sdir(indir + "/" + set + "/" + bufdir):
                        for file in os.listdir(indir + "/" + set + "/" + bufdir):
                            if file.find(name) >= 0 and file.find(".csv") >= 0: 
                                split_files.append(file)
                                split_dirs.append(indir + "/" + set + "/" + bufdir + "/")
                if bufdir.find("Text" + reverse + algo + "Splitted") >= 0:
                    if os.path.sdir(indir + "/" + set + "/" + bufdir):
                        for file in os.listdir(indir + "/" + set + "/" + bufdir):
                            if file.find(name) >= 0 and file.find(".txt"): 
                                split_texts.append(file)
        founds = True
        for i in range(len(split_files)):
            file = split_files[i].replace(".csv", ".txt")
            if qlibs.find(file, split_texts) < 0:
                founds = False
                qlibs.trace("union", split_dirs[i] + file, population)
        if founds == True:
            textdir = indir + "/" + set + "/Text" + reverse + "/" + fgr[2] + "/" + fgr[1] + "/"
            if name.find(".txt") < 0: textfile = textdir + name + ".txt" 
            fin = open(textfile, "r")
            text = fin.read()
            fin.close()
            csv = ""
            header = False
            print(split_files)
            for i in range(len(split_files)):
                textsplit = split_files[i].replace(".csv", ".txt")
                fin = open(split_dirs[i].replace(algo, "Text") + textsplit, "r")
                buf = fin.read()
                fin.close()
                offset = text.find(buf)
                print (split_files[i], offset)
                fin = open(split_dirs[i] + split_files[i], "r")
                buf = fin.read()
                fin.close()
                rows = buf.split("\n")
                if header == False:
                    csv = csv + rows[0] + "\n"
                    header = True
                for j in range(1, len(rows)):
                    cols = rows[j].split(";")
                    if len(cols) > 1:
                        cols[0] = str(int(cols[0]) + offset)
                        for col in cols: csv =csv + col + ";"
                        csv = csv + "\n"
            print (ucsvfile)
            print(csv)
            fout = open(ucsvfile, "w")
            fout.write(csv)
            fout.close()
            
            data = qlibs.get_uniquerows(ucsvfile, population)
            
            fout = open(csvufile, "w")
            fout.write(data)
            fout.close()
            


    return

def save_union(population, algo, reverse):
    indir = qlibs.get_datadir() + population + "/"
    sets = os.listdir(indir)
    print(sets)
    for set in sets:
        if os.path.isdir(indir + set):
            for dir in  os.listdir(indir + set + "/"):
                if dir.find(algo + reverse + "Splitted") >= 0:
                    if os.path.isdir(indir + set + "/" + dir + "/"):
                        for file in  os.listdir(indir + set + "/" + dir + "/"):
                            if file.find(".csv") > 0: union(indir, set, dir, file, population, algo, reverse)
    return

def txt_equals_csv(population, algo, reverse, count):
    splitted = ""
    for i in range(0, count):
        splitted = splitted + "Splitted"
    indir = qlibs.get_datadir() + population
    sets = os.listdir(indir)
    text = ""
    for set in sets:
        csvfiles = []
        txtfiles = []
        if os.path.isdir(indir + "/" + set):
            for dir in  os.listdir(indir + "/" + set):
                if dir.find(algo + reverse + splitted) >= 0:
                    if os.path.isdir(indir + "/" + set + "/" + dir + "/"):
                        for file in  os.listdir(indir + "/" + set + "/" + dir + "/"):
                            if file.find(".csv") > 0: csvfiles.append(file)
                if dir.find("Text" + reverse + algo + splitted) >= 0:
                    if os.path.isdir(indir + "/" + set + "/" + dir + "/"):
                        for file in  os.listdir(indir + "/" + set + "/" + dir + "/"):
                            if file.find(".txt") > 0: txtfiles.append(file)
            for file in txtfiles:
                if qlibs.find(file.replace(".txt", ".csv"), csvfiles) < 0: 
                    text = text + qlibs.get_datadir() + population + "/" + set + "/Text" + reverse + algo + splitted + "/" + file + "\n"
    if text == "": result = True
    else:
        outfile = get_filename(population, algo, count)
        fout = open(outfile, "w")
        fout.write(text)
        fout.close()
        result = False
    return result

def substr_not_founds(population, algo, overlap, reverse, nsplit = 2, libpath = ""):
    count = get_filecount(population, algo)
    if count <= 0: start_file(population, algo)
    else: count = count - 1
    infile = get_filename(population, algo, count)
    #logdir = qlibs.get_logdir() + population + "/"        
    fin = open (infile, "r")
    buf = fin.read()
    fin.close()
    lines = buf.split("\n")
    print(lines,  reverse)
    for line in lines:
        if line.find("C:/") >= 0 or line.find("./") >= 0:
            if line.find(".txt") >= 0:
                infile = qlibs.get_datadir() + line[line.find(population):]
                outfile = infile.replace("/Text", "/" + algo).replace(".txt", ".csv")
                buf = outfile[outfile.find(algo) :]
                length = buf.find("/") + 2
                outdir = outfile[:outfile.find("/" + algo) + length]
                print(population, line, infile, outfile, outdir, buf)
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                splittedoutfile = infile.replace("/Text" + reverse, "/Text" + reverse + algo + "Splitted")
                buf = splittedoutfile[splittedoutfile.find("Text" + reverse + algo  + "Splitted") :]  
                length = buf.find("/") + 2
                splittedoutdir = splittedoutfile[: splittedoutfile.find("/Text" + reverse + algo + "Splitted") + length]
                if not os.path.exists(splittedoutdir):
                    os.mkdir(splittedoutdir)
                if not os.path.exists(outfile):
                    if algo == "QgrsWeb":
                        if qgrs.qgrs_web(population, infile, outfile) == False:
                            found = False
                            try:
                                split_file(population, algo, infile, splittedoutdir, nsplit, overlap, reverse)
                            except:
                                pass
                    if algo == "Qgrs":
                        if platform.system().find("Windows") >= 0: libcpp = cdll.LoadLibrary("../lib/Qgrs.dll")
                        if platform.system().find("Linux") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-linux.a")
                        if platform.system().find("Darwin") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-mac.so")
                        if qgrs.qgrs_local(population, infile, outfile, libcpp) == False:
                            found = False
                            try:
                                split_file(population, algo, infile, splittedoutdir, nsplit, overlap, reverse)
                            except:
                                pass
                    if algo == "Pqs":
                        if qgrs.pqs(libpath, population, infile, outfile) == False:
                            found = False
                            try:
                                split_file(population, algo, infile, splittedoutdir, nsplit, overlap, reverse)
                            except:
                                pass
                else: 
                    print(outfile)
    count = count + 1
    result = txt_equals_csv(population, algo, reverse, count)    
    return  result                  
    


# Example: "AKAP17A__NM_005088___utci_0_split_1_split_0_split_0_split_0_split_0.txt"
