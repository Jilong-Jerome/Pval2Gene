import sys
if __name__ == "__main__":
    head_genes = sys.argv[1]
    snps_file = sys.argv[2]
    output_file = sys.argv[3]
    EXTENSION = 500000
    EXTEND_LABEL = 500000
    genes = open(head_genes)
    genes_dict={}
    gene_names=[]
    regions_list = []
    region_chr = 0
    region_start = 0
    region_end = 0
    previous_end = 0
    length = sum(1 for line in genes)
    genes.close()
    genes = open(head_genes)
    n = 0
    for gene in genes:
        n = n + 1
        gene_info = gene.strip("\n").split("\t")
        gene_ID = gene_info[0]
        gene_chr = gene_info[1]
        gene_start = gene_info[2]
        gene_end = gene_info[3]
        gene_names.append(gene_ID)
        genes_dict[str(gene_chr)+"\t"+str(gene_start)+"\t"+str(gene_end)] = gene_ID
        if gene_chr == region_chr:
            if n == length:
                region_end = int(gene_end) + EXTENSION
                regions_list.append(str(region_chr)+"\t"+str(region_start)+"\t"+str(region_end))
            else:
                if int(gene_start)-previous_end > EXTENSION:
                    regions_list.append(str(region_chr)+"\t"+str(region_start)+"\t"+str(region_end))
                    region_start = int(gene_start) - EXTENSION
                    previous_end = int(gene_end)
                    region_end = previous_end + EXTENSION
                else:
                    if int(gene_end) > previous_end:
                        previous_end = int(gene_end)
                        region_end = previous_end + EXTENSION
        else:
            if n == length:
                regions_list.append(str(region_chr)+"\t"+str(region_start)+"\t"+str(region_end))
                region_chr = gene_chr
                region_end = int(gene_end) + EXTENSION
                region_start = int(gene_start) - EXTENSION
                regions_list.append(str(region_chr)+"\t"+str(region_start)+"\t"+str(region_end))
            else:
                regions_list.append(str(region_chr)+"\t"+str(region_start)+"\t"+str(region_end))
                region_start = int(gene_start) - EXTENSION
                previous_end = int(gene_end)
                region_end = previous_end + EXTENSION
                region_chr = gene_chr
    genes.close()
    print("Creation of gene dictionary and Highlight Regison, finished")
    regions_list = regions_list[1:]
    print(regions_list)
    snps = open(snps_file)
    gene_count = {}
    flag = 0
    for gene in gene_names:
        gene_count[gene] = 0
    for snp in snps:
        if flag == 0:
            flag = 1
            pass
        else:
            snp_info = snp.split("\t")
            for key in genes_dict:
                if (snp_info[0] == key.split("\t")[0]) and (int(snp_info[1]) >= (int(key.split("\t")[1])-EXTEND_LABEL)) and (int(snp_info[1]) <= (int(key.split("\t")[2])+EXTEND_LABEL)):
                    gene_name = genes_dict[key]
                    if gene_name in gene_names:
                        gene_count[gene_name] = gene_count[gene_name] + 1
    snps.close()
    for gene in gene_count:
        gene_count[gene] = int(gene_count[gene]/2)
    print("Counting Snps overlapped by gene, finished")
    snps = open(snps_file)
    flag = 0
    file = open(output_file,'w')
    file.write("chr"+"\t"+"pos"+"\t"+"snp"+"\t"+"localscore"+"\t"+"is_highlighted"+"\t"+"is_annotated"+"\t"+"gene"+"\n")
    for snp in snps:
        if flag == 0:
            flag = 1
            pass
        else:
            snp_info = snp.strip("\n").split("\t")
            annotate_status = "no"
            highlight_status = "no"
            gene_name = ""
            for region in regions_list:
                if (snp_info[0] == region.split("\t")[0]) and (int(snp_info[1]) >= int(region.split("\t")[1])) and (int(snp_info[1]) <= int(region.split("\t")[2])):
                    highlight_status = "yes"
                    break
            for key in genes_dict:
                if (snp_info[0] == key.split("\t")[0]) and (int(snp_info[1]) >= (int(key.split("\t")[1])-EXTEND_LABEL)) and (int(snp_info[1]) <= (int(key.split("\t")[2])+EXTEND_LABEL)):
                    snp_info.append("")
                    gene_name = genes_dict[key]
                    if gene_count[gene_name] == 0:
                        annotate_status = "yes"
                        gene_count[gene_name] = gene_count[gene_name]-1
                        file.write(snp_info[0]+"\t"+snp_info[1]+"\t"+str(snp_info[0])+"_"+str(snp_info[1])
                       +"\t"+snp_info[2]+"\t"+highlight_status+"\t"+annotate_status+"\t"+gene_name+"\n")
                    else:
                        gene_count[gene_name] = gene_count[gene_name]-1
                        annotate_status = "no"
            if annotate_status == "no":
                file.write(snp_info[0]+"\t"+snp_info[1]+"\t"+str(snp_info[0])+"_"+str(snp_info[1])
                       +"\t"+snp_info[5]+"\t"+highlight_status+"\t"+annotate_status+"\t"+gene_name+"\n")
    print("merging, finished")
    file.close()
    snps.close()
