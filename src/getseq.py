#!/usr/bin/python3

import os
import re
import sys
import time
import datetime
import qlibs
import requests
import tkinter as tk

#
# Filename: getseq.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def params(argv):
    result = ["", "", "", False]
    nparams = 0
    feature = True
    split = False
    granularity = "&hgSeq.granularity=feature"
    casing = "&hgSeq.casing=upper"
    mask = "&boolshad.hgSeq.maskRepeats=0&hgSeq.repMasking=lower"
    for i in range(1, len(argv)):
        try:
            if argv[i].index(".csv")>= 0:
                result [0] = argv[i]
        except:
               pass
        if argv[i] == "-u":
            result [1] = result[1] + "&hgSeq.promoter=on&boolshad.hgSeq.promoter=0&hgSeq.promoterSize=" + argv[i+1]
            result [2] = result [2] + "Upstream" + argv[i+1]
            nparams = nparams + 1
        if argv[i] == "-f":
            result [1] = result [1] + "&hgSeq.utrExon5=on&boolshad.hgSeq.utrExon5=0"
            result [2] = result [2] + "UtrExon5"
            nparams = nparams + 1
        if argv[i] == "-c":
            result [1] = result [1] + "&hgSeq.cdsExon=on&boolshad.hgSeq.cdsExon=0"
            result [2] = result [2] + "CdsExon"
            nparams = nparams + 1
        if argv[i] == "-t":
            result [1] = result [1] + "&hgSeq.utrExon3=on&boolshad.hgSeq.utrExon3=0"
            result [2] = result [2] + "UtrExon3"
            nparams = nparams + 1
        if argv[i] == "-i":
            result [1] = result [1] + "&hgSeq.intron=on&boolshad.hgSeq.intron=0"
            result [2] = result [2] + "Intron"
            nparams = nparams + 1
        if argv[i] == "-d":
            result [1] = result[1] + "&hgSeq.downstream=on&boolshad.hgSeq.downstream=0&hgSeq.downstreamSize=" + argv[i+1]
            result [2] = result [2] + "Downstream" + argv[i+1]
            nparams = nparams + 1
        if argv[i] == "-s":
            result [1] = result [1] + "&hgSeq.splitCDSUTR=on&boolshad.hgSeq.splitCDSUTR=0"
            split = True
        if argv[i] == "-g":
            granularity = "&hgSeq.granularity=" + argv[i+1]
            feature = argv[i+1] != "gene"
        if argv[i] == "-h":
            casing = "&hgSeq.casing=" + argv[i+1]
        if argv[i] == "-m":
            masking = "&hgSeq.maskRepeats=on" + "&boolshad.hgSeq.maskRepeats=0&hgSeq.repMasking="+ argv[i+1]
        if argv[i] == "-n":
            result[3] = True
    print (nparams)
    if nparams == 6:
        result[2] = "FullGeneSeq"
    if feature == True:
        result[2] = result[2] + "OnePerRegion"
    if split == True:
        result [2] = result [2] + "SplitCDSUTR"
    print(result[2])
    result[1] = result[1] + granularity + casing + mask
    return result

def get_fasta_gene_alt(gene, code, search):
    try:
        url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + gene + "&hgt.positionInput=" + gene
        #url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + code + "&hgt.positionInput=" + code
        print(url)
        r = requests.get(url)
        html = r.text
        buf = html[html.index("NCBI RefSeq genes, curated subset (NM_*, NR_*, NP_* or YP_*)") : ]
        #buf = html[html.index("ncbiRefSeqCurated") : ]
        #buf = html[html.index("UCSC annotations of RefSeq RNAs (NM_* and NR_*)") : ]
        #print(buf)
        c = re.compile ("hgsid=\w+\&")
        i = c.findall(buf)
        sid = i[0][6: len(i[0]) - 1]
        #print (sid)
        pattern = code + "\.\d+ at chr[X-Y|\d]+\w+alt:\d+-\d+"
        c = re.compile(pattern)
        c.findall(buf)
        res = c.findall(buf)
        #print(res)
        c = re.compile("\.\d+")
        v = c.findall(res[0])
        value = v[0][1:]
        c = re.compile("chr[X-Y|\d]+\w+alt:\d+-\d+")
        ch = c.findall(res[0])
        chromosome = ch[0] #[3:]
        print(chromosome)
        c = re.compile(":\d+")
        #ll = c.findall(res[0])
        ll = c.findall(chromosome)
        l = ll[0][1:]
        print(l)
        c = re.compile("-\d+")
        #rr = c.findall(res[0])
        rr = c.findall(chromosome)
        r = rr[0][1:]
        print (r)
        code = code + "." + value
        ch = chromosome[:chromosome.find(":")]
        #print (code)
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(l)) + "&r=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(r))+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + ch + "&l=" + l + "&r=" + r+ "&getDnaPos=" + chromosome + search + "&submit=get+DNA"
        
        
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub(r'\d+', lambda m: '{:,}'.format(int(m.group(0))), l) + "&r=" + re.sub(r'd+', lambda m: '{:,}'.format(int(m.group(0))), r)+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcDnaNearGene&i="+ code + "&c="+ chromosome +"&l="+ str(l) + "&r="+ str(r) + search +  "&o=refGene&submit=submit"
        print (url)
        r = requests.get(url)
        html = r.text
        return html [html.index("<PRE>") + 5 : html.index("</PRE>")]
    except Exception as e:
        print (str(e))
        return ""

def get_fasta_alt(gene, code, search):
    try:
        #url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + gene + "&hgt.positionInput=" + gene
        url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + code + "&hgt.positionInput=" + code
        print(url)
        r = requests.get(url)
        html = r.text
        buf = html[html.index("NCBI RefSeq genes, curated subset (NM_*, NR_*, NP_* or YP_*)") : ]
        #buf = html[html.index("ncbiRefSeqCurated") : ]
        #buf = html[html.index("UCSC annotations of RefSeq RNAs (NM_* and NR_*)") : ]
        #print(buf)
        c = re.compile ("hgsid=\w+\&")
        i = c.findall(buf)
        sid = i[0][6: len(i[0]) - 1]
        #print (sid)
        pattern = code + "\.\d+ at chr[X-Y|\d]+\w+alt:\d+-\d+"
        c = re.compile(pattern)
        c.findall(buf)
        res = c.findall(buf)
        #print(res)
        c = re.compile("\.\d+")
        v = c.findall(res[0])
        value = v[0][1:]
        c = re.compile("chr[X-Y|\d]+\w+alt:\d+-\d+")
        ch = c.findall(res[0])
        chromosome = ch[0] #[3:]
        print(chromosome)
        c = re.compile(":\d+")
        #ll = c.findall(res[0])
        ll = c.findall(chromosome)
        l = ll[0][1:]
        print(l)
        c = re.compile("-\d+")
        #rr = c.findall(res[0])
        rr = c.findall(chromosome)
        r = rr[0][1:]
        print (r)
        code = code + "." + value
        ch = chromosome[:chromosome.find(":")]
        #print (code)
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(l)) + "&r=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(r))+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + ch + "&l=" + l + "&r=" + r+ "&getDnaPos=" + chromosome + search + "&submit=get+DNA"
        
        
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub(r'\d+', lambda m: '{:,}'.format(int(m.group(0))), l) + "&r=" + re.sub(r'd+', lambda m: '{:,}'.format(int(m.group(0))), r)+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcDnaNearGene&i="+ code + "&c="+ chromosome +"&l="+ str(l) + "&r="+ str(r) + search +  "&o=refGene&submit=submit"
        print (url)
        r = requests.get(url)
        html = r.text
        return html [html.index("<PRE>") + 5 : html.index("</PRE>")]
    except Exception as e:
        print (str(e))
        return ""


def get_fasta_gene(gene, code, search):
    try:
        url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + gene + "&hgt.positionInput=" + gene
        #url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + code + "&hgt.positionInput=" + code
        print(url)
        r = requests.get(url)
        html = r.text
        buf = html[html.index("NCBI RefSeq genes, curated subset (NM_*, NR_*, NP_* or YP_*)") : ]
        #buf = html[html.index("ncbiRefSeqCurated") : ]
        #buf = html[html.index("UCSC annotations of RefSeq RNAs (NM_* and NR_*)") : ]
        #print(buf)
        c = re.compile ("hgsid=\w+\&")
        i = c.findall(buf)
        sid = i[0][6: len(i[0]) - 1]
        #print (sid)
        pattern = code + "\.\d+ at chr[X-Y|\d]+:\d+-\d+"
        c = re.compile(pattern)
        c.findall(buf)
        res = c.findall(buf)
        #print(res)
        c = re.compile("\.\d+")
        v = c.findall(res[0])
        value = v[0][1:]
        c = re.compile("chr[X-Y|\d]+")
        ch = c.findall(res[0])
        chromosome = ch[0][3:]
        c = re.compile(":\d+")
        ll = c.findall(res[0])
        l = ll[0][1:]
        #print(l)
        c = re.compile("-\d+")
        rr = c.findall(res[0])
        r = rr[0][1:]
        #print (r)
        code = code + "." + value
        #print (code)
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(l)) + "&r=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(r))+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub(r'\d+', lambda m: '{:,}'.format(int(m.group(0))), l) + "&r=" + re.sub(r'd+', lambda m: '{:,}'.format(int(m.group(0))), r)+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcDnaNearGene&i="+ code + "&c="+ chromosome +"&l="+ str(l) + "&r="+ str(r) + search +  "&o=refGene&submit=submit"
        print (url)
        r = requests.get(url)
        html = r.text
        return html [html.index("<PRE>") + 5 : html.index("</PRE>")]
    except Exception as e:
        print (str(e))
        return ""



def get_fasta(gene, code, search):
    try:
        #url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + gene + "&hgt.positionInput=" + gene
        url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + code + "&hgt.positionInput=" + code
        print(url)
        r = requests.get(url)
        html = r.text
        buf = html[html.index("NCBI RefSeq genes, curated subset (NM_*, NR_*, NP_* or YP_*)") : ]
        #buf = html[html.index("ncbiRefSeqCurated") : ]
        #buf = html[html.index("UCSC annotations of RefSeq RNAs (NM_* and NR_*)") : ]
        #print(buf)
        c = re.compile ("hgsid=\w+\&")
        i = c.findall(buf)
        sid = i[0][6: len(i[0]) - 1]
        #print (sid)
        pattern = code + "\.\d+ at chr[X-Y|\d]+:\d+-\d+"
        c = re.compile(pattern)
        c.findall(buf)
        res = c.findall(buf)
        #print(res)
        c = re.compile("\.\d+")
        v = c.findall(res[0])
        value = v[0][1:]
        c = re.compile("chr[X-Y|\d]+")
        ch = c.findall(res[0])
        chromosome = ch[0][3:]
        c = re.compile(":\d+")
        ll = c.findall(res[0])
        l = ll[0][1:]
        #print(l)
        c = re.compile("-\d+")
        rr = c.findall(res[0])
        r = rr[0][1:]
        #print (r)
        code = code + "." + value
        #print (code)
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(l)) + "&r=" + re.sub("(\d)(?=(\d{3})+(?!\d))",r"\l,","%d" % int(r))+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub(r'\d+', lambda m: '{:,}'.format(int(m.group(0))), l) + "&r=" + re.sub(r'd+', lambda m: '{:,}'.format(int(m.group(0))), r)+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        #url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcDnaNearGene&i="+ code + "&c="+ chromosome +"&l="+ str(l) + "&r="+ str(r) + search +  "&o=refGene&submit=submit"
        print (url)
        r = requests.get(url)
        html = r.text
        return html [html.index("<PRE>") + 5 : html.index("</PRE>")]
    except Exception as e:
        print (str(e))
        return ""

def create_dir(basedir, indata):
    
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    basedir = basedir + "/Fasta/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    basedir = basedir + indata[2] + "/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    return basedir


def get_seq(population, argv):
    result = []
    basedir = qlibs.get_datadir() + population + "/"
    countfile = qlibs.get_datadir() + "Countfile.log"

    indata = params(argv)
    finput = indata[0]
    search = indata[1]
    col3rd = indata[3]
        
    if col3rd == False :
        basename = os.path.basename(indata[0])
        result.append(basename[:len(basename) - 4])
        datadir = basedir + basename[:len(basename) - 4]
        datadir = create_dir(datadir, indata)

    fin = open(finput, "r")
    buf = fin.read()
    fin.close()
    rows = buf.split("\n")

    try :
        fc = open(countfile, "r")
        buf = fc.read()
        fc.close()
        cols = buf.split("\t")
        count = int(cols[0])
        day = time.strptime(cols[3], "%Y-%m-%d")
        today = time.strptime(str(datetime.date.today()), "%Y-%m-%d")
        print(day, today)
        if today > day:
            count = 0
        elif count >= 5000: 
            tk.messagebox.showinfo("Quad", "Daily hits limit reached!")
            return result
        if cols[2] == finput:
            i = int(cols[1])
            if i >= len(rows):
                res = tk.messagebox.askyesno("Quad","WARNING:\n\n File already processed \n\n Do you want to force Execution?")
                if res == True:
                    i = 0
                    
        else:
            i = 0
    except:
        count = 0
        i = 0


    while i < len(rows):
        cols = rows[i].split(";")
        if len(cols) > 1:
            code = cols[0]
            gene = cols[1]
            if col3rd == True :
                if qlibs.find(cols[2], result) < 0: result.append(cols[2])
                datadir = basedir + cols[2]
                datadir = create_dir(datadir, indata)
            count = count + 1
            print(count, gene, code)
            text = get_fasta(gene, code, search)
            if text == "": 
                text = get_fasta_gene(gene, code, search)
                if text =="":
                    get_fasta_alt(gene, code, search)
                    if text =="":
                        text = get_fasta_gene_alt(gene, code, search)
                        if text =="": qlibs.trace("fasta", gene + "\t" + code, population)
                        else:
                            fout = open(datadir + gene + "__" + code + ".fasta", "w")
                            fout.write (text)
                            fout.close()
                    else:
                        fout = open(datadir + gene + "__" + code + ".fasta", "w")
                        fout.write (text)
                        fout.close()
                else:
                    fout = open(datadir + gene + "__" + code + ".fasta", "w")
                    fout.write (text)
                    fout.close()
            else:
                fout = open(datadir + gene + "__" + code + ".fasta", "w")
                fout.write (text)
                fout.close()
            if count % 5000 == 0:
                tk.messagebox.showinfo("Quad", "Daily hits limit reached!")
                break
            time.sleep(5)
        i = i + 1

    fc = open(countfile, "w")
    fc.write(str(count)+ "\t" + str(i) + "\t" + finput + "\t" + str(datetime.date.today()))
    fc.close()    
    return result