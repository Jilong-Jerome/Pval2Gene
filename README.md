# Pval2Gene
From a genome-wide p-value(or any other score) to clear manhattan plot with gene annotated.

## Introduction
The pipeline is originally built for the post analysis of the output result from GRoSS (Graph-aware Retrieval of Selective Sweeps, https://github.com/FerRacimo/GRoSS), which is described in the following paper: https://genome.cshlp.org/content/29/9/1506. However, the pipeline is also capable of managing the general genome-wide p-value dataset with 3 columns (CHR POS P-value/Score).
The GRoSS output includes the chi-squared statistics and the corresponding p-values for each branch of the admixture graph. This pipeline is applied for highlighting and gene annotation of significant candidate regions in a specific chosen branch.

For pinpointing the significant regions, this pipeline contains a P-value refinement process (local score process) which is introduced and realized from Fariello et.al 2017. https://onlinelibrary.wiley.com/doi/full/10.1111/mec.14141 Please cite this paper if you end up using this pipeline.  
After the local score process, genes are aligned to the significant regions (with 50kb extension on both sides) and annotated. The gene regions with a distance shorter than 500kb are merged into tracts to be highlighted.

Updates for general application still on the way, which includes:  
Genome-wide gene alignment and annotation for genes in top quantiles  
Options for applying local score approach or not  
Tolerance for user-defined chromosome choice  
## Preparation of Packages
R packages:
ggplot2
data.table
RColorBrewer
tidyverse
qqman
## Usage
Clone this respiratory and put both GRoSS output file and gene file in the folder of **codes**  
The branch name in GRoSS output file follows the following format: **Pval_EndNode_StartNode**  
An example of gene list for canid genomes are given in the **demos** folder.  
Then the pipeline can be done with a single line command as following.  
```
bash Local_Man.sh -g $GRoSS_Output -b $Branch_Name -m $Gene_List
```
The whole process may take some time, thus it is recommended to hang up the pipeline with "nohup" in Linux system.  
A series of datasets will be generated during the full process, at last the file named "branch_name.png" will be the figures similar to what in shown in the example.  

After analysis of several branches, you may be like to have a portable summary file for significant zones and genes overlapped in the relevant regions for all branches. This can be done with following steps:  
Generate a ``` filename.list ``` in tsv format, where in the 1st column are the ```.sigzone05``` files and in the 2nd column are the ```.sig.gene.sorted``` files like the example below.
```
Pval_Ancient_European_Dog_n4.sigzone05  Pval_Ancient_European_Dog_n4.dt.sig.gene.sorted
Pval_Eurasian_Wolf_n3.sigzone05 Pval_Eurasian_Wolf_n3.dt.sig.gene.sorted
Pval_european_Breed_Dog_a1.sigzone05    Pval_european_Breed_Dog_a1.dt.sig.gene.sorted
Pval_Sled_Dog_a3.sigzone05      Pval_Sled_Dog_a3.dt.sig.gene.sorted
Pval_South_China_Dog_a2.sigzone05       Pval_South_China_Dog_a2.dt.sig.gene.sorted
```
## Examples
Example of the result plot.
![](images/SLD_uniqe.png)
