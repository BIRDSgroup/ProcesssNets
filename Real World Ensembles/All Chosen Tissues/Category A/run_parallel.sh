B=1000
cores=10
counter=0

#tissues=("Whole_Blood" "Muscle_Skeletal" "Lung" "Skin_Sun_Exposed_Lower_leg" "Thyroid" "Pancreas" "Brain_Cortex" "Pituitary" "Brain_Cerebellum" "Stomach" "Brain_Caudate_basal_ganglia" "Kidney_Cortex" "Brain_Substantia_nigra" "Uterus" "Vagina" "Brain_Amygdala" "Whole_Blood_73" "Whole_Blood_237" "Muscle_Skeletal_237" "Muscle_Skeletal_73" "Lung_237" "Lung_73" "Skin_Sun_Exposed_Lower_leg_237" "Thyroid_237" "Skin_Sun_Exposed_Lower_leg_73" "Thyroid_73")

tissues=("Whole_Blood" "Muscle_Skeletal" "Lung" "Skin_Sun_Exposed_Lower_leg" "Thyroid" "Pancreas" "Brain_Cortex" "Pituitary" "Brain_Cerebellum" "Stomach")
echo "Generating Networks"
for tissue in "${tissues[@]}"; do
	echo $tissue
	time ./graphs.sh $tissue $B >> "output.txt" 2>> "error.txt"
done

echo "Starting the ProcessNets"
declare -A c
c["Whole_Blood"]=1
c["Muscle_Skeletal"]=6
c["Lung"]=11
c["Skin_Sun_Exposed_Lower_leg"]=16
c["Thyroid"]=21
c["Pancreas"]=26
c["Brain_Cortex"]=31
c["Pituitary"]=36
c["Brain_Cerebellum"]=41
c["Stomach"]=46
for tissue in "${tissues[@]}"; do
{
	echo $tissue
	folder="$tissue"
	cd ProcessNets
	start=${c[$tissue]}
	end=$((start + 4))
	taskset -c "$start"-"$end" time ./main.sh $folder -1 $B -1 $tissue >> "$folder/output.txt" 2>> "$folder/error.txt"
}&
((counter++)); ((counter % cores == 0)) && wait
done

exit
