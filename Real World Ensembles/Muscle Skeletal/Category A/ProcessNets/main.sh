tissue=$1
n=$2
B=$3
s=$4
gname=$5

root=$((2 * (B - 1)))

echo $tissue
cp -r graphs_$gname/* graphs_orig_$gname/

echo 'JSI Compute'
python -c "from Functions.tree import JSICompute; JSICompute($n, '$gname', '$tissue')" >> $tissue/'jsi.txt' 2>&1

echo 'Tree Construction'
#Tree Constructions
for tree in RSTAR SLINK FPA UPGMA WPGMC;
do
	mkdir $tissue/$tree
done

{
	echo "RSTAR TREE Construction"
	time python madi_tree_rstar.py $tissue $B $gname
} >> $tissue/'rstar.txt' 2>&1

for tree in slink fpa upgma wpgmc; do
{	
	rm -f graphs_$gname/*
	cp -r graphs_orig_$gname/* graphs_$gname/
	echo "${tree^^} TREE Construction"
	time python madi_tree_heuristics.py $tissue $B $tree $gname
	cp "graphs_$gname/$root.csv" "$tissue/${tree^^}/root.csv"
} >> $tissue/$tree'.txt' 2>&1
done

# Properties
cores=5
counter=0
for tree in rstar slink fpa upgma wpgmc; do
{
	echo "${tree^^} Degree"
	time python madi_measure.py $tissue $B $tree degree
			
	echo "${tree^^} Connectivity"
	time python madi_measure.py $tissue $B $tree connectivity
		
	echo "${tree^^} PageRank"
	time python madi_measure.py $tissue $B $tree pr
				
	#echo "${tree^^} Closeness"
	#time python madi_measure.py $tissue $B $tree cc
} >> $tissue/$tree'.txt' 2>&1 &
((counter++)); ((counter % cores == 0)) && wait
done

rm -f graphs_$gname/*
cp -r graphs_orig_$gname/* graphs_$gname/
#TRIVIAL APPROACH
{
	echo "TRIVIAL Degree"
	time python mytrivial_deg.py $tissue $B $gname
	
	echo "TRIVIAL Connectivity"
	time python mytrivial_con.py $tissue $B $gname
	
	echo "TRIVIAL PageRank"
	time python mytrivial_pr.py $tissue $B $gname
	
	#echo "TRIVIAL Closeness"
	#time python trivial_cc.py $tissue $B $gname
} >> $tissue/'mytrivial.txt' 2>&1

rm -f graphs_$gname/*
cp -r graphs_orig_$gname/* graphs_$gname/
#TRIVIAL APPROACH - networkx
{
	echo "TRIVIAL Degree"
	time python trivial_deg.py $tissue $B $gname
	
	echo "TRIVIAL Connectivity"
	time python trivial_con.py $tissue $B $gname
	
	echo "TRIVIAL PageRank"
	time python trivial_pr.py $tissue $B $gname
	
	#echo "TRIVIAL Closeness"
	#time python trivial_cc.py $tissue $B $gname
} >> $tissue/'trivial.txt' 2>&1

#DELETING INTERMEDIATE FILES
rm -r graphs_$gname
rm -r graphs_orig_$gname
