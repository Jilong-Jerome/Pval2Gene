library(readr)
library(tidyr)
library(dplyr)
library(ggplot2)
# List of SNPs to highlight are in the snpsOfInterest object
# We will use ggrepel for the annotation
library(ggrepel)

# Prepare the dataset
args <- commandArgs(T)
snps <- read_tsv(args[1],col_types = "ddcdccc")
snps <- snps %>% filter(chr != 39)
don <- snps %>% 
  
  # Compute chromosome size
  group_by(chr) %>% 
  summarise(chr_len=max(pos)) %>% 
  
  # Calculate cumulative position of each chromosome
  mutate(tot=cumsum(chr_len)-chr_len) %>%
  select(-chr_len) %>%
  
  # Add this info to the initial dataset
  left_join(snps, ., by=c("chr"="chr")) %>%
  
  # Add a cumulative position of each SNP
  arrange(chr, pos) %>%
  mutate( poscum=pos+tot)
  
  # Add highlight and annotation information
  #mutate( is_highlight=ifelse(SNP %in% snpsOfInterest, "yes", "no")) %>%
  #mutate( is_annotate=ifelse(-log10(P)>4, "yes", "no")) 

# Prepare X axis
axisdf <- don %>% group_by(chr) %>% summarize(center=( max(poscum) + min(poscum) ) / 2 )

# Make the plot
png(args[2],width = 2000, height = 800)
ggplot(don, aes(x=poscum, y=localscore)) +
  
  # Show all points
  geom_point( aes(color=as.factor(chr)), alpha=0.8, size=1.3) +
  scale_color_manual(values = rep(c("grey", "skyblue"), 22 )) +
  
  # custom X axis:
  scale_x_continuous( label = axisdf$chr, breaks= axisdf$center ) +
  scale_y_continuous(expand = c(0, 0) ) +     # remove space between plot area and x axis
  
  # Add highlighted points
  geom_point(data=subset(don, is_highlighted=="yes"), color="orange", size=2) +
  
  # Add label using ggrepel to avoid overlapping
  geom_label_repel( data=subset(don, is_annotated=="yes"), aes(label=gene), size=5) +
  
  # Custom the theme:
  theme_bw() + xlab("chromosome") +
  theme( 
    legend.position="none",
    text = element_text(size=20),
    panel.border = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.minor.x = element_blank()
  )
dev.off()
