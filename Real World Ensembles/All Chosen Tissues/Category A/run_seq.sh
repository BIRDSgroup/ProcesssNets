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
for tissue in "${tissues[@]}"; do
{
	echo $tissue
	folder="$tissue"
	cd ProcessNets
	time ./main.sh $folder -1 $B -1 $tissue >> "$folder/output.txt" 2>> "$folder/error.txt"
	cd ..
}
done

exit
