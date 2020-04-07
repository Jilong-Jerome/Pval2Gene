import sys
def summary_files(filelist,outname):
    files_list = open(filelist)
    extension = 50000
    output_dict = {}
    for file in files_list:
        files = file.strip("\n").split("\t")
        branch_name = files[0].strip("Pval_").strip(".sigzone05")
        zone_file = files[0]
        gene_file = files[1]
        active_zones=[]
        zones = open(zone_file)
        genes = open(gene_file)
        next(zones)
        for zone in zones:
            zone = zone.strip("\n").split("\t")
            if float(zone[3]) != 0:
                active_zones.append([zone[0],zone[1],zone[2],branch_name])
        for zone in active_zones:
            output_dict[" ".join(map(str,zone))] = []
        for gene in genes:
            gene = gene.split("\t")
            chr = gene[1]
            start  = int(gene[2]) - extension
            end = int(gene[3]) + extension
            for zone in active_zones:
                if chr == zone[0]:
                    if end < int(zone[1]) or start > int(zone[2]):
                        pass
                    else:
                        output_dict[" ".join(zone)].append(gene[0])
    output = open(outname,"w")
    for each in output_dict:
        gene_pool = output_dict[each]
        output.write(each.replace(" ","\t"))
        output.write("\t")
        output.write(" ".join(gene_pool))
        output.write("\n")
if __name__ == "__main__":
    filelist = sys.argv[1]
    outname = sys.argv[2]
    summary_files(filelist,outname)
