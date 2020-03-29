#title: "R script for computing local scores"



### **Description**: 
## Detecting genomic outliers in a sequence of correlated scores, from Fariello et al 2017.

### Import libraries.
library(ggplot2)
library(data.table)
library(RColorBrewer)
library(tidyr)
library(dplyr)
library(readr)
library(qqman)
#Import functions.
source('scorelocalfunctions.R')


### Import toy data.

#Data should be organized as one locus per line and three columns
#chromosome number | position | score
#The first line of the table should include the names: chr pos pval

#The p-values of the used statistic should follow a uniform distribution. 
#If this is not the case, then new coefficients of the Gumbel Law should be computed. 
args = commandArgs(T)
mydata = fread(args[1], head=T, select=c('chr', 'pos','pval'))
genome_data <- read_tsv(args[1])
Nrow <- NROW(genome_data)
Nrow
mydata$pval[mydata$pval==0]=1e-16
pvalue <- genome_data$pval
genome_cor = autocor(pvalue)
genome_cor
setkey(mydata, chr)
Nchr=length(mydata[,unique(chr)])

### Computation of absoulte position in the genome. 

#This is useful for doing genomewide plots. 

chrInfo=mydata[,.(L=.N,cor=autocor(pval)),chr]
setkey(chrInfo,chr)
data.table(chr=mydata[,unique(chr),], S=cumsum(c(0,chrInfo$L[-Nchr]))) %>% 
  setkey(.,chr) %>% mydata[.,posT:=pos+S]

### Choice of $\xi$

# To choose the apropiate threshold ($\xi = 1, \dots, 4$) we look at the distribution of 鈭抣og10(p 鈭? value). 
#Then the score function will be $鈭抣og10(p 鈭? value) 鈭? \xi$. 

# In this case we choose $\xi$ = 1, as there are not values above 2.
# Remember that we have to choose some value between mean(-log10(mydata$pval)) and max(-log10(mydata$pval)).


## Computation of the score and the Lindley Process

# We should verify that the mean of the score is negative. 
#It should be according to the chosen value of xi.

#Set the chosen xi!!
xi=1
mydata[,score:= -log10(pval)-xi]
# The score mean must be negative
mean(mydata$score)
mydata[,lindley:=lindley(score),chr]

# Compute significance threshold for each chromosome

## Uniform distribution of p-values

#If the distribution of the p-values is uniform and if $\xi=$ is 1, 2, 3 or 4, 
#it is possible to compute the significancy thresholds for each chromosome directely, 
#given the length and the autocorrelation of the chromosome .


#############################################################################
######## Run only if the distribution of your p-values is not uniform  ######
#############################################################################


## If the distribution of the p-values is not uniform, then a re-sampling strategy should be used. 

coefsG=coefsGumb(mydata, Ls=seq(30000,60000,10000), nSeq=5000)

chrInfo[,thG05:=threshold(Nrow, genome_cor, coefsG$aCoef, coefsG$bCoef,0.05),]
chrInfo[,thG01:=threshold(Nrow, genome_cor, coefsG$aCoef, coefsG$bCoef,0.01),]


#chrInfo[,':=' (thG05=threshold(Nrow, genome_cor, coefsG$aCoef, coefsG$bCoef,0.05), thG01=threshold(Nrow, genome_cor, coefsG$aCoef, coefsG$bCoef,0.01)),]

mydata=mydata[chrInfo]

sigZones05=mydata[,sig_sl(lindley, pos, unique(thG05)),chr]
sigZones01=mydata[,sig_sl(lindley, pos, unique(thG01)),chr]
write_tsv(sigZones05,paste(args[1],".sigzone05",sep=""))

pdf(paste(args[1],'.pdf',sep=""))
par(mfrow=c(4,1), mar=c(5,2,1,1))
for (g in chrInfo$chr){
  plot(mydata[chr==g,pos],mydata[chr==g,lindley],xlab=paste("position chr",g,sep=' '),ylab="Score Local", type='l', ylim=c(0,max(mydata[chr==g,max(lindley)],mydata[chr==g, unique(thG01)])))
  abline(h=mydata[chr==g, unique(thG05)], col='grey')
  abline(h=mydata[chr==g, unique(thG01)], lty=2, col='grey')
  abline(v=sigZones01[chr==g, beg], col='grey', lty=3)
  abline(v=sigZones01[chr==g, end], col='grey', lty=3)
  }
dev.off()
write_tsv(mydata,paste(args[1],'.dt',sep=""))
png(paste(args[1],'manhattan.png',sep=""),width = 2000,height = 800)
manhattan(mydata, chr = "chr", bp = "pos", p = "lindley", logp = FALSE, ylab = "Localscore", genomewideline = FALSE, 
          suggestiveline = FALSE, main = "Genome-wide Localscore")
dev.off()
