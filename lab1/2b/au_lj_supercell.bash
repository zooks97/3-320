#!/bin/bash

# set run name
runname="au_lj"

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
"lennard 12 6\n"\
"Au core Au core 214108.2 625.482 40.0 0 0\n"\
        > $runname"_supercell.temp"
    # run buildcell
    ./buildcell.py $runname"_supercell.temp"
    rm $runname"_supercell.temp"
done

# write input files for supercell with vacancy relax
echo "VACANCY CALCULATIONS"
for cell in "${cellsize[@]}";
do
    echo $cell  # uncomment to print cell size at each step
    echo -e \
"4.077 Au "$cell" true\n"\
"opti dist comp conp\n"\
"lennard 12 6\n"\
"Au core Au core 214108.2 625.482 40.0 0 0\n"\
        > $runname"_relax.temp"
    # run buildcell
    ./buildcell.py $runname"_relax.temp"
    rm $runname"_relax.temp"
done

# run gulp
for file in *.in; do
    gulp < $file > $(basename $file .in).out
done

# parse output files
grep "Total lattice energy" -m 1 *supercell*out > supercell.dat
grep "Final energy" -m 1 *relax*.out > relax.dat
paste supercell.dat relax.dat > $runname.dat
rm relax.dat supercell.dat

# plot energy vs lattice parameter
./vacancy_plot.py $runname.dat

echo -e "Done.\n"
