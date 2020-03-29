from IDprocesser_dog import *
from math import *
import sys
if __name__ == "__main__":
    snps_file = sys.argv[1]
    genes_file = sys.argv[2]
    output_file = sys.argv[3]
    snps_list = readinCoordinates(snps_file)
    GenomeDict = Create_genedict(genes_file, 50000, 39)
    gene_scores = {}
    for chromenum in GenomeDict:
        dict = GenomeDict[chromenum]
        for key in dict:
            gene_scores[dict[key]] = []
    i = 0
    for snp in snps_list:
        if snp[0] == 39:
            pass
        else:
            if snp[2] > 0:
                subdict = GenomeDict[str(snp[0])]
                for key in subdict:
                    up = int(key.split("\t")[0])
                    down = int(key.split("\t")[1])
                    if (snp[1] >= up) and (snp[1] <= down):
                        geneID = subdict[key]
                        gene_scores[geneID].append(-log10(snp[2]))
    genes_final = {}
    for gene in gene_scores:
        if gene_scores[gene]:
            genes_final[gene] = max(gene_scores[gene])
    file = open(output_file, 'w')
    for gene in genes_final:
        file.write(gene + "\t" + str(genes_final[gene]) + "\n")
    file.close()
