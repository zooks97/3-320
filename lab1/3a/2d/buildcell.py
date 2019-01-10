#!/usr/bin/python3

import sys
import textwrap
import pymatgen
import numpy as np

if __name__ == '__main__':
    # parse input file
    assert len(sys.argv) == 2
    infile = sys.argv[1]
    with open(infile, 'r') as f:
        infile_lines = f.readlines()

    system_info = infile_lines[0].strip().split()
    lattice_constant, specie, supercell_size, vacuum = system_info
    
    # create structure information
    fcc_sites = np.array([[0.0, 0.0, 0.0],
                          [0.0, 0.5, 0.5],
                          [0.5, 0.0, 0.5],
                          [0.5, 0.5, 0.0]])
    species = [specie for site in fcc_sites]
    lattice = float(lattice_constant) * np.eye(3)
    structure = pymatgen.Structure(lattice, species, fcc_sites)
   
    # create a slab 1 layer thick in the z direction
    supercell_size = int(supercell_size)
    supercell = structure * np.array([supercell_size, supercell_size, 1])
    supercell_sites = [site.frac_coords for site in supercell.sites]
    supercell_species = [site.specie.symbol for site in supercell.sites]

    # add vacuum
    vacuum = float(vacuum)
    supercell_lattice = [supercell.lattice.a,
                         supercell.lattice.b,
                         supercell.lattice.c + vacuum,
                         supercell.lattice.alpha,
                         supercell.lattice.beta,
                         supercell.lattice.gamma]

    
    # write supercell input file for gulp
    supercell_infile = infile.split('.')[0] +\
                           '_{}_{}.in'.format(vacuum, supercell_size)
    leading_instructions = infile_lines[1]
    trailing_instructions = '\n'.join(infile_lines[2:])
    site_instructions = []
    for site, specie in zip(supercell_sites, supercell_species):
        site_instruction = '{} {:4f} {:4f} {:4f}'.format(specie, *site)
        site_instructions.append(site_instruction)
    site_instructions = '\n'.join(site_instructions)
    structure_instructions = textwrap.dedent(
        '''
        cell
        {:4f} {:4f} {:4f} {:2f} {:2f} {:2f}
        fractional
        {}
        ''').format(*supercell_lattice, site_instructions)
    supercell_infile_text = leading_instructions + \
                            structure_instructions + \
                            trailing_instructions
    
    with open(supercell_infile, 'w') as f:
        f.write(supercell_infile_text)

