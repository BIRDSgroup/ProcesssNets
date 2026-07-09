# Variation with respect to n and s
echo "Variation with respect to n and s"
cores=10
counter=0
B=1000
for n in $(seq 100 100 1000); do
	echo $n
	mkdir -p ProcessNets/$n
	time python SIM_graphs_s.py $n $n $B >> "ProcessNets/$n/output.txt" 2>> "ProcessNets/$n/error.txt"
	
	declare -A c
	c[75]=1
	c[100]=6
	c[150]=11
	c[200]=16
	c[300]=21
	c[500]=26
	c[600]=31
	c[700]=36
	c[1000]=41
	c[1500]=46
	for s in 75 100 150 200 300 500 600 700 1000 1500; do
	{
		echo $n $s
		folder="$n/$s"
		mkdir -p ProcessNets/graphs_$s ProcessNets/$folder ProcessNets/graphs_orig_$s
		cp $s/[0-9]*.csv ProcessNets/graphs_$s
		cp "$s/edge count.tsv" ProcessNets/$folder
		cp ProcessNets/$n/seed.txt ProcessNets/$folder
		rm -r $s
		
		cd ProcessNets
		start=${c[$s]}
		end=$((start + 4))
		taskset -c "$start"-"$end" time ./main.sh $folder $n $B $s $s >> "$folder/output.txt" 2>> "$folder/error.txt"
	} &
	((counter++)); ((counter % cores == 0)) && wait
	done
	#cd ..
	echo "$n Done"
done
echo "Done"

exit
