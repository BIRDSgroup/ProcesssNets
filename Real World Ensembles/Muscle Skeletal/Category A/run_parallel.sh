B=1000
#tissues=("Whole_Blood" "Muscle_Skeletal" "Lung" "Skin_Sun_Exposed_Lower_leg" "Thyroid" "Pancreas" "Brain_Cortex" "Pituitary" "Brain_Cerebellum" "Stomach" "Brain_Caudate_basal_ganglia" "Kidney_Cortex" "Brain_Substantia_nigra" "Uterus" "Vagina" "Brain_Amygdala" "Whole_Blood_73" "Whole_Blood_237" "Muscle_Skeletal_237" "Muscle_Skeletal_73" "Lung_237" "Lung_73" "Skin_Sun_Exposed_Lower_leg_237" "Thyroid_237" "Skin_Sun_Exposed_Lower_leg_73" "Thyroid_73")

tissues=("Muscle_Skeletal")
for tissue in "${tissues[@]}"; do	
	for n in $(seq 100 100 1000); do
		echo $n
		time ./graphs.sh $tissue $B $n >> "output.txt" 2>> "error.txt"
		echo "Starting the ProcessNets"
		cd ProcessNets
		taskset -c 1-10 time ./main.sh $tissue $n $B -1 $tissue
		mv "$tissue" "$n"
		cd ..
	done
	mkdir -p $tissue
	for n in $(seq 100 100 1000); do
    		mv "ProcessNets/$n" "$tissue/"
	done
done
exit
