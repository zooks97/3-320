#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

# parse data
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    bulk_energy = float(lines[0].strip().split()[-2])

with open(sys.argv[2], 'r') as f:
    dat = f.readlines()

vacuums, surface_energies = [], []
for line in dat:
    line = line.strip().split()
    vacuum = float(line[0].split('_')[-2])
    vacuum_energy = float(line[5])
    # calculate surface energy
    surface_energy = np.abs(vacuum_energy - bulk_energy) / \
            (4.077**2)
    vacuums.append(vacuum)
    surface_energies.append(surface_energy)

# plot supercell size vs formation energy
fig = plt.figure()
plt.xlabel('vacuum')
plt.ylabel('surface energy (eV/A**2)')
plt.scatter(vacuums, surface_energies, marker='o')
plt.savefig('2d_vacuum.png', format='png')
plt.show()
