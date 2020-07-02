#!/usr/bin/python3

import os
import qlibs

#
# Filename: seqslost.py
# Author: Saverio Simonelli <saverio.simonelli.95@gmail.com>
# Copyright: 2020 Saverio Simonelli 
# License: MIT license
#

def getlost(infile, population, set):
    datadir = qlibs.get_datadir()
    outdir = datadir + "Lost/" + set + "/"
    outfile = outdir + "/lost_" + set + ".csv"
    qlibs.create_path(outdir)
    rows = qlibs.get_rows(infile)
    text = ""
    for row in rows:
        cols = row.split(";")
        if len(cols) > 1:
            code = cols[0]
            gene = cols[1]
            found = False
            indir = qlibs.get_datadir() + population + "/" + set + "/Text/"
            for region in os.listdir(indir):
                if os.path.isdir(indir + region):
                    datadir = indir + region + "/" + gene + "__" + code
                    if os.path.isdir(datadir):
                        found = True
            if found == False: text += code + ";" + gene + ";\n"
    ft = open(outfile, "w")
    ft.write(text)
    ft.close()
    return 

def getlost_fromerrors(infile, population, set):
    datadir = qlibs.get_datadir()
    outdir = datadir + "Lost/" + set + "/"
    outfile = outdir + "/declost_" + set + ".csv"
    qlibs.create_path(outdir)
    rows = qlibs.get_rows(infile)
    text = ""
    for row in rows:
        cols = row.split("\t")
        if len(cols) > 1:
            codebuf = cols[1]
            gene = cols[0]
            buf = codebuf.split(".")
            if int(buf[1]) > 1: 
                code = buf[0] + "." + str(int(buf[1]) - 1)
                text += code + ";" + gene + ";\n"
    ft = open(outfile, "a")
    ft.write(text)
    ft.close()
    return 


def get_fasta(gene, code, search):
    try:
        url = "https://genome.ucsc.edu/cgi-bin/hgTracks?position=" + gene + "&hgt.positionInput=" + gene
        r = requests.get(url)
        html = r.text
        #buf = html[html.index("NCBI RefSeq genes, curated subset (NM_*, NR_*, NP_* or YP_*)") : ]
        buf = html[html.index("ncbiRefSeqCurated") : ]
        c = re.compile ("hgsid=\w+\&")
        i = c.findall(buf)
        sid = i[0][6: len(i[0]) - 1]
        #print (sid)
        pattern = code + " at chr\d+:\d+-\d+"
        c = re.compile(pattern)
        c.findall(buf)
        res = c.findall(buf)
        c = re.compile("chr\d+")
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
        url = "https://genome.ucsc.edu/cgi-bin/hgc?hgsid=" + sid + "&g=htcGetDna2&table=ncbiRefSeqCurated&i=" + code +"&o=ncbiRefSeqCurated&c=" + chromosome + "&l=" + re.sub(r'\d+', lambda m: '{:,}'.format(int(m.group(0))), l) + "&r=" + re.sub(r'd+', lambda m: '{:,}'.format(int(m.group(0))), r)+ "&getDnaPos=chr" + chromosome + ":" + l + "-" + r + search + "&submit=get+DNA"
        r = requests.get(url)
        html = r.text
        return html [html.index("<PRE>") + 5 : html.index("</PRE>")]
    except Exception as e:
        print (str(e))
        return ""

def get_seq(population, finput, search):
    result = []
    basedir = qlibs.get_datadir() + population + "/"
    search = indata[1]
    fin = open(finput, "r")
    buf = fin.read()
    fin.close()
    rows = buf.split("\n")
    i = 0


    while i < len(rows):
        cols = rows[i].split(";")
        if len(cols) > 1:
            code = cols[0]
            gene = cols[1]
            text = get_fasta(gene, code, search)
            if text == "": qlibs.trace("lostfasta", gene + "\t" + code, population)
            else:
                fout = open(datadir + gene + "__" + code + ".fasta", "w")
                fout.write (get_fasta(gene, code, search))
                fout.close()
            time.sleep(5)
        i = i + 1
  
    return result
