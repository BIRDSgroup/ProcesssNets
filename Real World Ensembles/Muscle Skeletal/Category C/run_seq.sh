B=1000
cores=6
counter=0
tissue="Muscle_Skeletal"
echo "Generating Graphs"
for sp in $(seq 70 5 95); do
	time ./graphs.sh $tissue $B $sp >> "output.txt" 2>> "error.txt"
done

echo "Starting ProcessNets"
for sp in $(seq 70 5 95); do
{
	echo $sp
	folder="$sp"
	cd ProcessNets
	time ./main.sh $folder -1 $B -1 $sp >> "$folder/output.txt" 2>> "$folder/error.txt"
	cd ..
}
done
echo "Done"

mkdir $tissue
mv ProcessNets/[0-9]* $tissue/
exit
