# Variation with respect to n and s
echo "Variation with respect to n and B"
cores=10
counter=0
s=500
for n in $(seq 100 100 1000); do
	echo $n
	mkdir ProcessNets/$n
	time python SIM_graphs_B.py $n $n $s >> "ProcessNets/$n/output.txt" 2>> "ProcessNets/$n/error.txt"	
	for B in $(seq 100 100 1000); do
	{
		echo $n $B
		folder="$n/$B"
		mkdir ProcessNets/graphs_$B ProcessNets/$folder ProcessNets/graphs_orig_$B
		cp $B/[0-9]*.csv ProcessNets/graphs_$B
		cp "$B/edge count.tsv" ProcessNets/$folder
		cp ProcessNets/$n/seed.txt ProcessNets/$folder
		rm -r $B
		
		cd ProcessNets
		time ./main.sh $folder $n $B $s $B >> "$folder/output.txt" 2>> "$folder/error.txt"
		cd ..
	}
	done	
	echo "$n Done"
done
echo "Done"

exit

