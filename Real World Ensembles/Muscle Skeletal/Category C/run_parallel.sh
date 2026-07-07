B=1000
cores=6
counter=0
tissue="Muscle_Skeletal"
echo "Generating Graphs"
for sp in $(seq 70 5 95); do
	time ./graphs.sh $tissue $B $sp >> "output.txt" 2>> "error.txt"
done

echo "Starting ProcessNets"
declare -A corenum
corenum[70]=1
corenum[75]=6
corenum[80]=11
corenum[85]=16
corenum[90]=21
corenum[95]=26
for sp in $(seq 70 5 95); do
{
	echo $sp
	folder="$sp"
	cd ProcessNets
	start=${corenum[$sp]}
	end=$((start + 4))
	taskset -c "$start"-"$end" time ./main.sh $folder -1 $B -1 $sp >> "$folder/output.txt" 2>> "$folder/error.txt"
}&
((counter++)); ((counter % cores == 0)) && wait
done
echo "Done"

mkdir $tissue
mv ProcessNets/[0-9]* $tissue/
exit
