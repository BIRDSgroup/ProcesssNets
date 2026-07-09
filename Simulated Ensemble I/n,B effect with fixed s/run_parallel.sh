# Variation with respect to n and s
echo "Variation with respect to n and B"
cores=10
counter=0
s=500
for n in $(seq 100 100 1000); do
	echo $n
	mkdir -p ProcessNets/$n
	time python SIM_graphs_B.py $n $n $s >> "ProcessNets/$n/output.txt" 2>> "ProcessNets/$n/error.txt"
	declare -A c
	c[100]=1
	c[200]=6
	c[300]=11
	c[400]=16
	c[500]=21
	c[600]=26
	c[700]=31
	c[800]=36
	c[900]=41
	c[1000]=46
	for B in $(seq 100 100 1000); do
	{
		echo $n $B
		folder="$n/$B"
		mkdir -p ProcessNets/graphs_$B ProcessNets/$folder ProcessNets/graphs_orig_$B
		cp $B/[0-9]*.csv ProcessNets/graphs_$B
		cp "$B/edge count.tsv" ProcessNets/$folder
		cp ProcessNets/$n/seed.txt ProcessNets/$folder
		rm -r $B
		
		cd ProcessNets
		start=${c[$B]}
		end=$((start + 4))
		taskset -c "$start"-"$end" time ./main.sh $folder $n $B $s $B >> "$folder/output.txt" 2>> "$folder/error.txt"
	} &
	((counter++)); ((counter % cores == 0)) && wait
	done
	#cd ..
	echo "$n Done"
done
echo "Done"

exit

