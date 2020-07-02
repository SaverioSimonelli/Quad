#libpath = 'C:/Users/Utente/Documents/R/win-library/3.5'

log = function(population){
	logdir = "./log/"
	if(!dir.exists(logdir)){
		logdir = "../log/"
		if(!dir.exists(logdir)){
			logdir = "../../log/"
		}
	}
	logdir = paste(logdir, population, sep="")
	logdir = paste(logdir, "/", sep="")
	if(!dir.exists(logdir)){
		dir.create(logdir)
	}
	return(logdir)
}

logtrace = function(population, txt){
	filename = paste(log(population), "pqs_error", gsub("-", "", Sys.Date()), ".log", sep="")
	write(txt, filename, append=TRUE)
}

analyze = function(libpath, population, infile, outfile){
	tryCatch({
		library(BiocGenerics, lib.loc=libpath)
		library(S4Vectors, lib.loc=libpath)
		library(IRanges, lib.loc=libpath)
		library(XVector, lib.loc=libpath)
		library(Biostrings, lib.loc=libpath)
		library(pqsfinder, lib.loc=libpath)
		doc=read.table(file=infile)
		seq <- DNAString(doc[1,1])
		pqs <- pqsfinder(seq) #, max_len = 100L)
		dfseq <- as.data.frame(pqs)
		colnames(dfseq) <- c("seq")
		df = data.frame()
		df = cbind("start"=start(pqs), "width"=width(pqs), "strand"=strand(pqs), "score"=score(pqs),dfseq)
		write.csv2(df,file=outfile)
	},
	error = function(e) {
		logtrace(population, infile)
		logtrace(population, paste("",e))
	})
}


args <- commandArgs(trailingOnly = TRUE)
#infile = args[2]
#outfile = args[3]
#population = args[1]
#analize(population, infile, outfile)
#population <- "/5ConditionsAnalysis"
#textdir <- "../data/5ConditionsAnalysis/ADIPO_CO-COLT_HG vs ADIPO_HG_177genes/Text/"
#textdir <- "../data/5ConditionsAnalysis/ADIPO_CO-COLT_HG-LG vs ADIPO_HG-LG_129genes/Text/"
#textdir <- "../data/5ConditionsAnalysis/ADIPO_HG-LG vs ADIPO_HG_87genes/Text/"
#textdir <- "../data/5ConditionsAnalysis/MCF7_CO-COLT_HG vs MCF7_HG_121genes/Text/"
#textdir <- "../data/5ConditionsAnalysis/MCF7_CO-COLT_HG-LG vs MCF7_HG-LG_25genes/Text/"
#regions <- "Upstream5000;Downstream5000;UtrExon3;UtrExon5;Intron"
#algo <- "Pqs"
libpath <- args[1]
population = args[2]
infile <- args[3]
outfile <- args[4]
analyze(libpath, population, infile, outfile)

