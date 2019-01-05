#!/bin/bash

# set run name
runname="gulp1b2"

# define lattice parameters
parameters=( 4.06 4.07 4.08 4.09 4.10)

# write input files
for lat in "${parameters[@]}";
do
    # echo $lat  # uncomment to print lat at each step
    echo -e \
"single dist comp conp\n"\
"cell\n"\
$lat" "$lat" "$lat" 90 90 90\n"\
"fractional\n"\
"Au 0.0 0.0 0.0\n"\
"Au 0.0 0.5 0.5\n"\
"Au 0.5 0.0 0.5\n"\
"Au 0.5 0.5 0.0\n"\
"library suttonchen\n"\
"dump "$runname"_"$lat".grs\n"\
    > $runname"_"$lat".in"
done

# run gulp
for file in *.in; do
    gulp < $file > $(basename $file .in).out
done

# parse output files
grep " a =" -m 1 *out > lattice.dat
grep "Total lattice energy" -m 1 *out > energy.dat
paste lattice.dat energy.dat > $runname.dat
rm lattice.dat energy.dat

# plot energy vs lattice parameter
gnuplot <<- EOF
    set xlabel "lattice parameter (A)"
    set ylabel "energy (eV)"
    set term png
    set output "${runname}.png"
    plot "${runname}.dat" using 4:13 with points pointtype 5
EOF

echo -e "Done.\nPlot saved in "$runname".png."
