# Variation with respect to n and p
echo "Variation with respect to n and p"
cores=7
counter=0
B=1000
for n in $(seq 100 100 1000); do
	echo $n
	mkdir -p ProcessNets/$n $n
	time python SIM_graphs_p.py $n $n $B >> "ProcessNets/$n/output.txt" 2>> "ProcessNets/$n/error.txt"
	echo $n
	folder="$n"
	mkdir -p ProcessNets/graphs_$n ProcessNets/graphs_orig_$n
	cp $n/[0-9]*.csv ProcessNets/graphs_$n
	cp "$n/edge count.tsv" ProcessNets/$folder
	rm -r $n
	
	cd ProcessNets
	taskset -c 1-5 time ./main.sh $folder $n $B $n $n >> "$folder/output.txt" 2>> "$folder/error.txt"	
	cd ..
done
echo "Done"

exit

