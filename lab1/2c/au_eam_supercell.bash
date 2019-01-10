#!/bin/bash

# set run name
runname="au_eam"

# define cell sizes
cellsize=( 2 3 4 5 6 7 8)

# write input files for supercell without vacancy
echo "SUPERCELL CALCULATIONS"
for cell in "${cellsize[@]}";
do
    echo $cell  # uncomment to print cell size at each step
    echo -e \
"4.077 Au "$cell" false\n"\
"single dist comp conp\n"\
"library suttonchen\n"\
"dump "$runname"_"$cell".grs\n"\
        > $runname"_supercell.temp"
    # run buildcell
    ./buildcell.py $runname"_supercell.temp"
    rm $runname"_supercell.temp"
done

# write input files for supercell with vacancy
echo "VACANCY CALCULATIONS"
for cell in "${cellsize[@]}";
do
    echo $cell  # uncomment to print cell size at each step
    echo -e \
"4.077 Au "$cell" true\n"\
"single dist comp conp\n"\
"library suttonchen\n"\
"dump "$runname"_"$cell".grs\n"\
        > $runname"_vacancy.temp"
    # run buildcell
    ./buildcell.py $runname"_vacancy.temp"
    rm $runname"_vacancy.temp"
done

for file in *.in; do
    gulp < $file > $(basename $file .in).out
done

# parse output files
grep "Total lattice energy" -m 1 *supercell*out > supercell.dat
grep "Total lattice energy" -m 1 *vacancy*.out > vacancy.dat
paste vacancy.dat supercell.dat > $runname.dat
rm vacancy.dat supercell.dat

# plot energy vs lattice parameter
./vacancy_plot.py $runname.dat

echo -e "Done.\n"
