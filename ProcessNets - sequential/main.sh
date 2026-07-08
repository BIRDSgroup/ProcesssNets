tissue=$1
n=$2
B=$3
s=$4
gname=$5
shift 5

# Defaults
config=(rstar slink fpa upgma wpgmc)
measure=(degree connectivity pr cc)
tself=T
tnx=T

# Parse optional arguments
while (($#)); do
    case "$1" in
        --config)
            config=()
            shift
            while (($#)) && [[ "$1" != --* ]]; do
                config+=("$1")
                shift
            done
            ;;
        --measure)
            measure=()
            shift
            while (($#)) && [[ "$1" != --* ]]; do
                measure+=("$1")
                shift
            done
            ;;
        --tself)
            shift            
            tself="$1"
            shift
            ;;
        --tnx)
            shift
            tnx="$1"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done


root=$((2 * (B - 1)))

echo $tissue
cp -r graphs_$gname/* graphs_orig_$gname/

echo 'JSI Compute'
python -c "from Functions.tree import JSICompute; JSICompute($n, '$gname', '$tissue')" >> $tissue/'jsi.txt' 2>&1

echo 'Tree Construction'
#Tree Constructions
for tree in "${config[@]}"; do
    dir="${tree^^}"   # Convert to uppercase
    mkdir -p "$tissue/$dir"
done

for tree in "${config[@]}"; do
	rm -f graphs_$gname/*
	cp -r graphs_orig_$gname/* graphs_$gname/		
    if [[ "$tree" == "rstar" ]]; then
		{
			echo "RSTAR TREE Construction"
			time python madi_tree_rstar.py $tissue $B $gname
		} >> $tissue/'rstar.txt' 2>&1
    else
		{
			echo "${tree^^} TREE Construction"
			time python madi_tree_heuristics.py $tissue $B $tree $gname
			cp "graphs_$gname/$root.csv" "$tissue/${tree^^}/root.csv"
		} >> $tissue/$tree'.txt' 2>&1
    fi
done

# Properties
cores=${#config[@]}
counter=0

for tree in "${config[@]}"; do
    {
        for prop in "${measure[@]}"; do
            echo "${tree^^} ${prop} MEASURE"
            time python madi_measure.py $tissue $B $tree $prop
        done
    } >> "$tissue/$tree.txt" 2>&1
done


rm -f graphs_$gname/*
cp -r graphs_orig_$gname/* graphs_$gname/
#TRIVIAL APPROACH
if [[ "$tself" == "T" ]]; then
    {
        for prop in "${measure[@]}"; do
            case "$prop" in
                degree)
                    echo "TRIVIAL Degree"
					time python mytrivial_deg.py $tissue $B $gname
                    ;;
                connectivity)
                    echo "TRIVIAL Connectivity"
					time python mytrivial_con.py $tissue $B $gname
                    ;;
				pr)
                    echo "TRIVIAL PageRank"
					time python mytrivial_pr.py $tissue $B $gname
                    ;;
				cc)
                    echo "TRIVIAL Closeness"
					time python trivial_cc.py $tissue $B $gname
                    ;;                
                *)
                    echo "Unknown measure: $prop"
                    ;;
            esac
        done
    } >> "$tissue/mytrivial.txt" 2>&1
fi

rm -f graphs_$gname/*
cp -r graphs_orig_$gname/* graphs_$gname/
#TRIVIAL APPROACH - networkx
if [[ "$tnx" == "T" ]]; then
    {
        for prop in "${measure[@]}"; do
            case "$prop" in
                degree)
                    echo "TRIVIAL Degree"
					time python trivial_deg.py $tissue $B $gname
                    ;;
                connectivity)
                    echo "TRIVIAL Connectivity"
					time python trivial_con.py $tissue $B $gname
                    ;;
				pr)
                    echo "TRIVIAL PageRank"
					time python trivial_pr.py $tissue $B $gname
                    ;;
				cc)
                    echo "TRIVIAL Closeness"
					time python trivial_cc.py $tissue $B $gname
                    ;;                
                *)
                    echo "Unknown measure: $prop"
                    ;;
            esac
        done
    } >> $tissue/'trivial.txt' 2>&1
fi

#DELETING INTERMEDIATE FILES
#rm -r graphs_$gname
rm -r graphs_orig_$gname
