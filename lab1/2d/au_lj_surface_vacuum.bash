#!/bin/bash

# set run name
runname="au_lj_vacuum"

# define cell sizes
vacuum=( 2.0385 4.077 6.1155 8.154 12.231 16.308 20.385 24.462 28.539)

# write input files for supercell without vacancy
echo "Vacuum CALCULATIONS"
for vacuum in "${vacuum[@]}";
do
    echo $vacuum  # uncomment to print cell size at each step
    echo -e \
"4.077 Au 1 "$vacuum"\n"\
"single dist comp conp\n"\
"lennard 12 6\n"\
"Au core Au core 214108.2 625.482 40.0 0 0\n"\
        > $runname".temp"
    # run buildcell
    ./buildcell.py $runname".temp"
    rm $runname".temp"
done

for file in *.in; do
    gulp < $file > $(basename $file .in).out
done

# parse output files
grep "Total lattice energy" -m 1 *supercell*.out > supercell.dat
grep "Total lattice energy" -m 1 *vacuum*.out > vacuum.dat
paste vacuum.dat supercell.dat > $runname.dat
rm vacuum.dat supercell.dat

# plot energy vs lattice parameter
# ./vacuum_plot.py $runname.dat

echo -e "Done.\n"
