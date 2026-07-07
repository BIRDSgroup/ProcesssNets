# Variation with respect to n and s
echo "Variation with respect to n and s"
cores=10
counter=0
B=1000
for n in $(seq 100 100 1000); do
	echo $n
	mkdir ProcessNets/$n
	time python SIM_graphs_s.py $n $n $B >> "ProcessNets/$n/output.txt" 2>> "ProcessNets/$n/error.txt"
	
	for s in 75 100 150 200 300 500 600 700 1000 1500; do
	{
		echo $n $s
		folder="$n/$s"
		mkdir ProcessNets/graphs_$s ProcessNets/$folder ProcessNets/graphs_orig_$s
		cp $s/[0-9]*.csv ProcessNets/graphs_$s
		cp "$s/edge count.tsv" ProcessNets/$folder
		cp ProcessNets/$n/seed.txt ProcessNets/$folder
		rm -r $s
		
		cd ProcessNets
		time ./main.sh $folder $n $B $s $s >> "$folder/output.txt" 2>> "$folder/error.txt"
		cd ..
	}
	done
	echo "$n Done"
done
echo "Done"

exit
