library("tidyr")
library("dplyr")
library("readr")
args <- commandArgs(T)
filename <- args[1]
genes <- read_tsv(filename,col_names = F)
genes <- genes %>% arrange(X2,X3)
write_tsv(genes,paste(filename,".sorted",sep=""),col_names = F)
