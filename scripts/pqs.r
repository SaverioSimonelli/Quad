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

analyze = function(population, infile, outfile){
	tryCatch({
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

save_csv <- function(libpath, population, textdir, regions, algo){
	tryCatch({
		library(BiocGenerics, lib.loc=libpath)
		library(S4Vectors, lib.loc=libpath)
		library(IRanges, lib.loc=libpath)
		library(XVector, lib.loc=libpath)
		library(Biostrings, lib.loc=libpath)
		library(pqsfinder, lib.loc=libpath)
		csvdir = sub("Text", "Pqs", textdir)
		if(!dir.exists(csvdir))	dir.create(csvdir)
		lst_regs <- unlist(strsplit(regions, ";"))
		print(lst_regs)
		for(region in lst_regs){
			if(region != ""){
				print(region)
				if(!dir.exists(paste(csvdir, region, sep="")))dir.create(paste(csvdir, region, sep=""))
				gene_codes <- list.dirs(paste(textdir, region, sep=""), full.name=FALSE)
				for(gene_code in gene_codes){
					if(gene_code != ""){
						if(!dir.exists(paste(csvdir, region, "/", gene_code, "/", sep=""))) dir.create(paste(csvdir, region, "/", gene_code, "/", sep=""))
						files <- list.files(paste(textdir, region, "/",  gene_code, "/", sep=""))
						for(fname in files){
							infile = paste(textdir, region, "/", gene_code, "/", fname, sep="")
							outfile = paste(csvdir, region, "/", gene_code, "/" , sub(".txt", ".csv", fname), sep="")
							analyze(population, infile, outfile)
							print(infile)
						}
					}
				}
			}
		}
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
textdir <- args[3]
regions <- args[4]
algo <- args[5]
save_csv(libpath, population, textdir, regions, algo)

