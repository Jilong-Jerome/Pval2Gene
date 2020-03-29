def readinCoordinates(snp_info):
    '''
    Read in SNP chromosome coordinates file to a list of tuplesf
    :param SNP_location:first column is chromosome number ,second is location
    :param Neoscan_Score:Scores corresponding to the order of SNP file
    :return:list of tuples of chromosome number, location and score
    '''
    snps_file=open(snp_info)
    snps_list=[]
    flag =0
    for snp in snps_file:
        if flag == 0:
            flag = 1
            pass
        else:
            snplist=snp.split('\t')
            chr = int(snplist[0])
            pos=int(snplist[1])
            pval=float(snplist[2])
            score = float(snplist[5])
            snps_list.append((chr,pos,pval,score))
    snps_file.close()
    return snps_list

def Create_genedict(genes_info_list,extend,chrnum):
    '''

    :param gene_id_list:gene info list
    :return:whole gene dict
    '''
    genes_Info=open(genes_info_list)
    GenomeDicts = locals()
    for i in range(chrnum):
        GenomeDicts["Subdict"+ str(i+1)] = {}
    SubdictX={}
    SubdictY = {}
    GenomeDict = {}
    for i in range(chrnum):
        subdict_name = "Subdict" + str(i + 1)
        GenomeDict[str(i+1)] = eval(subdict_name)
    GenomeDict["X"] = SubdictX
    GenomeDict["Y"] = SubdictY
    flag=0
    for gene in genes_Info:
        if (flag==0):
            flag=1
            pass
        else:
            geneinfolist=gene.split('\t')
            upstream50000 = int(geneinfolist[3])-extend
            downstream50000 = int(geneinfolist[4])+extend+1
            if str(geneinfolist[5]) != "":
                GenomeDict[str(geneinfolist[2])][str(upstream50000)+"\t"+str(downstream50000)] = str(geneinfolist[5])+"\t"+str(geneinfolist[2])+"\t"+str(geneinfolist[3])+"\t"+str(geneinfolist[4])
    genes_Info.close()
    return GenomeDict
