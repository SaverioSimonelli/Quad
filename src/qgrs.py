#!/usr/bin/python3

from ctypes import *
from xml.etree import ElementTree
import os
import sys
import qlibs
import requests
import datetime
import platform
import subprocess

#
# Filename: qgrs.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#
         
def qgrs_local(population, in_file, out_file, libcpp):
    try:
        infile = create_string_buffer(str.encode(in_file))
        outfile = create_string_buffer(str.encode(out_file))
        libcpp.qgrs(infile, outfile)
        return True
    except Exception as e:      
        qlibs.trace("qgrs_local", in_file, population)
        qlibs.trace("qgrs_local", str(e), population)
        return False

def qgrs_web(population, infile, outfile):
    try:
        url = "http://bioinformatics.ramapo.edu/QGRS/"
        fin = open(infile, "r")
        text = fin.read()
        fin.close()
        print(infile)
        if outfile.find("/QgrsWeb") < 0:
            webfile = outfile.replace("/Qgrs", "/QgrsWeb")
        else: webfile = outfile
        data = {'sequence': text}
        cookies = dict(QGRSmax='45',GGroupmin='2')
        r = requests.post(url + "analyze.php", data=data, cookies=cookies)
        html = r.text
        try: 
            buf = html[ html.index("dataview.php?") : ]
            url = url + buf[ : buf.index(" ")].replace("'", "").replace("\"", "")
        except Exception as e:
            print(str(e),"1")
            qlibs.trace("qgrsweb", str(datetime.datetime.now()), population)
            qlibs.trace("qgrsweb", infile, population)
            qlibs.trace("qgrsweb", str(e), population)
            return False
        r = requests.get(url)
        html = r.text
        try:
            html = ("<table>" + html[ html.index("<tr>") :  ]).replace("class=grey", "") 
        except Exception as e:
            print(str(e),"2")
            html = ""
            return False
            
        header = "ID;T1;T2;T3;T4;TS;GS;  SEQ;\n"
        csv = header
        csvweb = "Position;Length;QGRS;G-Score;\n"
        tree = ElementTree.fromstring(html)
        rows = tree.findall('tr')
        for i in range(1, len(rows)):
            seq = ""
            cols = ElementTree.fromstring(ElementTree.tostring(rows[i]))
            for j in range(len(cols)):
                buf = str(ElementTree.tostring(cols[j]), 'utf-8')
                buf = buf.replace("<td>", "").replace("</td>", "")
                try:
                    if buf.index("<u>") >= 0: seq = buf.replace("<u>", "").replace("</u>", "").replace("<b>", "").replace("</b>", "")
                    buf = seq
                except Exception as e: 
                    if j == 0: csv = csv + str(i) + ";" + buf + ";"
                    if j == 1: csv = csv + "0;0;0;0;"
                    if j == 3: csv = csv + buf + ";"
                csvweb = csvweb + buf + ";"
            csvweb = csvweb + "\n"
        fout = open (webfile, "w")
        fout.write(csvweb)
        fout.close()
        return True
    except Exception as e:
        qlibs.trace("qgrsweb", infile)
        qlibs.trace("qgrsweb", str(e))
        return False

def pqs(libpath, population, infile, outfile):
    try:
        script = qlibs.get_scriptsdir() + "analyze.r"
        cmd = ["Rscript", script] + [libpath, population, infile, outfile]
        result = subprocess.check_output(cmd, universal_newlines = True)
        print (result)
        return True
    except: return False

def save_csv(population, textdir, regions, algo, reverse):
    basedir = textdir[ : textdir.index("Text")]
    csvdir = basedir + algo + reverse + "/"
    webdir = basedir + "QgrsWeb" + reverse + "/"
    print(os.path.exists(csvdir))
    if not os.path.exists(csvdir):
        os.mkdir(csvdir)
    if not os.path.exists(webdir):
        os.mkdir(webdir)
    region = regions.replace(";","")
    if region.find("UtrExon5UtrExon3CdsExonIntron") >= 0:
        if region.find("Upstream") >= 0:
            if region.find("Downstream") >= 0: region = "FullGeneSeq"
    if not os.path.exists(csvdir + region):
        os.mkdir(csvdir + region)
    if not os.path.exists(webdir + region):
        os.mkdir(webdir + region)
    for r, d, f in os.walk(textdir + region):
        for gene_code in d:
            if not os.path.exists(csvdir + region + "/" + gene_code + "/"):
                os.mkdir(csvdir + region + "/" + gene_code + "/")
            if not os.path.exists(webdir + region + "/" + gene_code + "/"):
                os.mkdir(webdir + region + "/" + gene_code + "/")
            for r, d, f in os.walk(textdir + region  + "/" + gene_code + "/"):
                for fname in f:
                    infile = textdir + region  + "/" + gene_code + "/" + fname
                    outfile = csvdir + region + "/" + gene_code + "/" + fname[ : len(fname) - 4] + ".csv"
                    if algo == "QgrsWeb": qgrs_web(population, infile, outfile)
                    if algo == "Qgrs":
                        if platform.system().find("Windows") >= 0: libcpp = cdll.LoadLibrary("../lib/Qgrs.dll")
                        if platform.system().find("Linux") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-linux.a")
                        if platform.system().find("Darwin") >= 0: libcpp = cdll.LoadLibrary("../lib/qgrs-mac.so")
                        qgrs_local(population, infile, outfile, libcpp)
                    if algo == "Pqs": pqs(population, infile, outfile) 
                    
libcpp = None