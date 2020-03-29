import sys
def create_zone(sigzone):
    zones = open(sigzone)
    flag = 0
    zonelist=[]
    for zone in zones:
        if flag ==0:
            flag = 1
            pass
        else:
            zone = zone.strip("\n").split("\t")
            if (zone[1]!="0"):
                zonelist.append(zone)
    return zonelist
def get_sig(snps_file,sigzone,output_file,thredshold = 0.05):
    zonelist = create_zone(sigzone)
    print(zonelist)
    snps = open(snps_file)
    out = open(output_file,"w")
    flag = 0
    if thredshold == 0.05:
        num = 8
    elif thredshold == 0.01:
        num = 9
    for snp in snps:
        if flag == 0:
            flag = 1
            out.write(snp)
            pass
        else:
            snp = snp.strip("\n").split("\t")
            add_flag = 0
            for zone in zonelist:
                if snp[0] == zone[0]:
                    if (float(snp[1]) >= float(zone[1])) and (float(snp[1])<=float(zone[2])):
                        add_flag = 1
            if add_flag == 1:
                for i in range(len(snp)):
                    if i == len(snp) - 1:
                        out.write(snp[i])
                        out.write("\n")
                    else:
                        out.write(snp[i])
                        out.write("\t")
    snps.close()
    out.close()
if __name__ == "__main__":
    snps_file = sys.argv[1]
    output_file = sys.argv[3]
    sigzone_file = sys.argv[2]
    get_sig(snps_file,sigzone_file,output_file)
