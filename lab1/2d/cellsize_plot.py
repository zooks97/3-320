#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

# parse data
with open(sys.argv[1], 'r') as f:
    dat = f.readlines()

supercell_sizes, surface_energies = [], []
for line in dat:
    line = line.strip().split()
    supercell_size = int(line[0].split('_')[-1].split('.')[0])
    cellsize_energy = float(line[5])
    supercell_energy = float(line[-2])
    # calculate surface energy
    surface_energy = np.abs(cellsize_energy - supercell_energy) / \
            (supercell_size**2 * 4.077**2)
    supercell_sizes.append(supercell_size)
    surface_energies.append(surface_energy)

# plot supercell size vs formation energy
fig = plt.figure()
plt.xlabel('supercell size')
plt.ylabel('surface formation energy (eV)')
plt.scatter(supercell_sizes, surface_energies, marker='o')
plt.savefig('2d.png', format='png')
plt.show()
