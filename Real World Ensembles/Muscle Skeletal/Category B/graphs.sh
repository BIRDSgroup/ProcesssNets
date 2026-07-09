#!/bin/bash
#$ -cwd
#$ -o outputfile.txt
#$ -e errorfile.txt

tissue=$1
B=$2
n=$3
cores=50

echo $tissue $B
mkdir -p $tissue
mkdir -p ProcessNets/graphs_$tissue ProcessNets/graphs_orig_$tissue

#SEED GENERATION
echo "Seed Generation + Gene Expression Extraction"
mkdir seeds
Rscript seed.R $tissue $B

#BOOTSTRAPPING
echo 'Bootstrapping'
counter=0
for b in `seq 1 $B`
do
    echo $b
    time python compute.py $tissue $((b-1)) $n &
    ((counter++)); ((counter % cores == 0)) && wait
done

#INTERMEDIATE FILES
mv $tissue ProcessNets/
rm -r seeds

