#!/bin/bash

# set run name
runname="au_lj_surface"

# define cell sizes
cellsize=( 1 2 3 4 5 6)

# write input files for supercell without vacancy
echo "SUPERCELL CALCULATIONS"
for cell in "${cellsize[@]}";
do
    echo $cell  # uncomment to print cell size at each step
    echo -e \
"4.077 Au "$cell" 0.000\n"\
"single dist comp conp\n"\
"lennard 12 6\n"\
"Au core Au core 214108.2 625.482 40.0 0 0\n"\
        > $runname"_supercell.temp"
    # run buildcell
    ./buildcell.py $runname"_supercell.temp"
    rm $runname"_supercell.temp"
done

# write input files for supercell with vacancy
echo "SURFACE CELL SIZE CALCULATIONS"
for cell in "${cellsize[@]}";
do
    echo $cell  # uncomment to print cell size at each step
    echo -e \
"4.077 Au "$cell" 8.154\n"\
"single dist comp conp\n"\
"lennard 12 6\n"\
"Au core Au core 214108.2 625.482 40.0 0 0\n"\
        > $runname"_cellsize.temp"
    # run buildcell
    ./buildcell.py $runname"_cellsize.temp"
    rm $runname"_cellsize.temp"
done

for file in *.in; do
    gulp < $file > $(basename $file .in).out
done

# parse output files
grep "Total lattice energy" -m 1 *supercell*.out > supercell.dat
grep "Total lattice energy" -m 1 *cellsize*.out > cellsize.dat
paste cellsize.dat supercell.dat > $runname.dat
rm cellsize.dat supercell.dat

# plot energy vs lattice parameter
./cellsize_plot.py $runname.dat

echo -e "Done.\n"
