#!/usr/bin/python3

import os
import qlibs
import graphs
import datetime
import pandas as pan

#
# Filename: dist.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def dist_data(rootdir, setdir, algodir, reverse, outfile, popfile="", regiondir = "any", popfirst = False):
    set = []
    set.append(setdir)
    data = pan.DataFrame()
    first = True
    header = ["set","gene","code","region","#"]
    headset = ["gene","code","region","#"]
    basedir = rootdir + setdir + "/" + algodir + reverse + "/"
    for r, d, f in os.walk(basedir):
        for region in d:
            if region == regiondir or regiondir == "any":
                for r, dd, f in os.walk(basedir + region + "/"):
                    for gene_code in dd:
                        for r, d, f in os.walk(basedir + region  + "/" + gene_code + "/"):
                            
                            for fname in f:
                                listbuf = []
                                empty = True
                                print(setdir + "\t" + fname)
                                buf = gene_code.split("__")
                                listbuf.append(buf[0])
                                listbuf.append(buf[1])
                                if region.find("Upstream") >= 0 or region.find("Downstream") >= 0:
                                    index = region.find("Upstream")
                                    if index >= 0:
                                        no = region[index + 8 : ]
                                        listbuf.append("Upstream")
                                        listbuf.append(no)
                                    index = region.find("Downstream")
                                    if index >= 0: 
                                        no = region[index + 10 : ]
                                        listbuf.append("Downstream")
                                        listbuf.append(no)
                                else:   
                                    bb = fname.split("___")
                                    buff = bb[1].split("_")
                                    no = buff[1][:buff[1].find(".csv")]
                                    listbuf.append(region)
                                    listbuf.append(no)
                                infile = basedir + region  + "/" + gene_code + "/" + fname
                                try:
                                    indata = pan.read_csv(infile, sep = ";",index_col=False)
                                    count = indata.shape[0]
                                    indata = pan.DataFrame.join(pan.DataFrame(count*[listbuf], columns = headset), indata)
                                    if first == True:
                                        indata.to_csv(outfile, index = False, header = True,sep =  ";")
                                        first = False
                                    else:
                                        indata.to_csv(outfile,mode = "a", index = False, header = False,sep =  ";")
                                    if popfile != "":
                                        count = indata.shape[0]
                                        data = pan.DataFrame.join(pan.DataFrame(count*[set], columns = ["set"]), indata)
                                        print(popfirst, popfile)
                                        if popfirst == True:
                                            print(popfirst)
                                            data.to_csv(popfile, index = False, header = True, sep =  ";")
                                            popfirst = False
                                        else:
                                            data.to_csv(popfile,mode = "a", index = False, header = False,sep =  ";")
                                except Exception as e:
                                    qlibs.trace("dist", str(datetime.date.today()))
                                    qlibs.trace("dist", infile)
                                if empty == True: qlibs.trace("dist", infile)

    return popfirst

def dist(root, algodir, reverse, regiondir = "any", setdir = "any"):
    data = pan.DataFrame()
    dist = pan.DataFrame()
    header = True
    rootfile = ""
    datadir = qlibs.get_datadir()
    rootdir = datadir + root + "/"
    popfirst = True
    for set in os.listdir(rootdir):
        if os.path.isdir(rootdir + set):
            if set == setdir or setdir == "any":
                outfile = rootdir + set + "/" + "dist_" + algodir + reverse + "_" + root + "_" + set + "_YYYYmmdd.csv"
                newfile = rootdir + set + "/" + "dist_" + algodir + reverse + "_" + root + "_" + set + "_" + str(datetime.date.today()).replace("-", "") + ".csv"
                if setdir == "any":
                    rootfile = rootdir + "dist_" + algodir + reverse + "_" + root + "_YYYYmmdd.csv"
                    popfirst = dist_data(rootdir, set, algodir, reverse, outfile, rootfile, regiondir, popfirst)
                else:
                    dist_data(rootdir, set, algodir, reverse, outfile, regiondir)
                if os.path.isfile(outfile): 
                    if os.path.isfile(newfile): os.remove(newfile)
                    os.rename(outfile, newfile)
    if rootfile != "":
        newrootfile = rootdir + "dist_" + algodir + reverse + "_" + root + "_" + str(datetime.date.today()).replace("-", "") + ".csv"
        if os.path.isfile(rootfile): 
            if os.path.isfile(newrootfile): os.remove(newrootfile)
            os.rename(rootfile, newrootfile)
        pass
    return    
      
