library(readr)
library(tidyr)
library(dplyr)
args = commandArgs(T)
all_data <- read.delim(args[1])
chosen_data<- all_data %>% mutate(chr = CHR, pos = START,pval = get(args[2]))%>%select(chr,pos,pval)
write_tsv(chosen_data, paste('./',args[2],sep=""))

