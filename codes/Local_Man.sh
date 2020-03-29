#!/bin/bash
echo "$@"
while getopts ":g:b:m:" opt; do
  case $opt in
    g)
      GROSS=$OPTARG
      echo "GRoSS file: $GROSS"
      ;;
    b)
      BRANCH=$OPTARG
      echo "Chosen branch: $OPTARG"
      ;;
    m)
      GENELIST=$OPTARG 
      echo "Gene List: $OPTARG"
      ;;
    :)
      echo "Option -$OPTARG requires an argument." 
      exit 1
      ;;
    ?)
      echo "Invalid option: -$OPTARG"
      ;;
  esac
done
echo "Generate the subset of the chosen branch"
Rscript choosebranch.R $GROSS $BRANCH
echo "Chossing Branch Finished"
echo "Runing localscore method, may take some time"
Rscript mylocal_genome.R $BRANCH
echo "Local score process finished"
echo "Extract data from significant zones of local score method"
python get_significant_peaks.py $BRANCH.dt $BRANCH.sigzone05 $BRANCH.dt.sig
echo "Extraction of significant zones finished"
echo "Aligh genes overlapped with significant zones"
python IDprocess_dog_nosex.py $BRANCH.dt.sig $GENELIST $BRANCH.dt.sig.gene
echo "Gene alignment finished"
echo "Gene soring"
Rscript sort_genes.R $BRANCH.dt.sig.gene
echo "Merging dataset for plotting"
python merge_for_manhattan_version3.py $BRANCH.dt.sig.gene.sorted $BRANCH.dt $BRANCH.dt.merged
echo "Merging Done"
echo "Final Plotting"
Rscript manhattan_with_genes.R $BRANCH.dt.merged $BRANCH.png
echo "Finished all !!"
