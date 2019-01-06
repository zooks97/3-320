#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

# parse data
with open(sys.argv[1], 'r') as f:
    dat = f.readlines()

supercell_sizes, formation_energies = [], []
for line in dat:
    line = line.strip().split()
    supercell_size = int(line[0].split('_')[-1].split('.')[0])
    vacancy_energy = float(line[5])
    supercell_energy = float(line[12])
    # calculate formation energy
    formation_energy = vacancy_energy -\
                       (supercell_size - 1) / supercell_size *\
                       supercell_energy
    supercell_sizes.append(supercell_size)
    formation_energies.append(formation_energy)

# plot supercell size vs formation energy
fig = plt.figure()
plt.xlabel('supercell size')
plt.ylabel('vacancy formation energy (eV)')
plt.plot(supercell_sizes, formation_energies, marker='o')
plt.savefig('21.png', format='png')
