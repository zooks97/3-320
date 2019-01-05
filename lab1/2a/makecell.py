#!/usr/bin/python3

# The MIT License (MIT) Copyright (c) 2011-2012 MIT & LBNL

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

import numpy as np

# function from pymatgen.util.coord
def lattice_points_in_supercell(supercell_matrix):
    """
    Returns the list of points on the original lattice contained in the
    supercell in fractional coordinates (with the supercell basis).
    e.g. [[2,0,0],[0,1,0],[0,0,1]] returns [[0,0,0],[0.5,0,0]]

    Args:
        supercell_matrix: 3x3 matrix describing the supercell

    Returns:
        numpy array of the fractional coordinates
    """
    diagonals = np.array(
        [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1],
         [1, 1, 0], [1, 1, 1]])
    d_points = np.dot(diagonals, supercell_matrix)

    mins = np.min(d_points, axis=0)
    maxes = np.max(d_points, axis=0) + 1

    ar = np.arange(mins[0], maxes[0])[:, None] * \
         np.array([1, 0, 0])[None, :]
    br = np.arange(mins[1], maxes[1])[:, None] * \
         np.array([0, 1, 0])[None, :]
    cr = np.arange(mins[2], maxes[2])[:, None] * \
         np.array([0, 0, 1])[None, :]

    all_points = ar[:, None, None] + br[None, :, None] + cr[None, None, :]
    all_points = all_points.reshape((-1, 3))

    frac_points = np.dot(all_points, np.linalg.inv(supercell_matrix))

    tvects = frac_points[np.all(frac_points < 1 - 1e-10, axis=1)
                         & np.all(frac_points >= -1e-10, axis=1)]
    assert len(tvects) == round(abs(np.linalg.det(supercell_matrix)))
    return tvects

# adapted function from pymatgen.core.structure.Structure
def create_supercell(sites, lattice, scale_matrix):
    """
    Makes a supercell. Allowing to have sites outside the unit cell

    Args:
        sites: A Nx3 matrix of fractional x y z coordinates of atoms
        lattice: A 3x3 lattice matrix
        scaling_matrix: A scaling matrix for transforming the lattice
            vectors. Has to be all integers. Several options are possible:

            a. A full 3x3 scaling matrix defining the linear combination
               the old lattice vectors. E.g., [[2,1,0],[0,3,0],[0,0,
               1]] generates a new structure with lattice vectors a' =
               2a + b, b' = 3b, c' = c where a, b, and c are the lattice
               vectors of the original structure.
            b. An sequence of three scaling factors. E.g., [2, 1, 1]
               specifies that the supercell should have dimensions 2a x b x
               c.
            c. A number, which simply scales all lattice vectors by the
               same factor.

    Returns:
        new_sites: A Nx3 matrix of fractional x y z coordinates of atoms
            in the new supercell lattice
        new_lattice: A 3x3 lattice matrix of the new supercell lattice
    """
    scale_matrix = np.array(scaling_matrix, np.int16)
    if scale_matrix.shape != (3, 3):
        scale_matrix = np.array(scale_matrix * np.eye(3), np.int16)
    new_lattice = np.dot(scale_matrix, self._lattice.matrix)

    f_lat = lattice_points_in_supercell(scale_matrix)
    c_lat = np.dot(f_lat, new_lattice)

    new_sites = []
    for site in sites:
        for v in c_lat:
            c_s = site + v  # cartesian
            f_s = np.dot(cart_s, np.linalg.inv(c_lat))
            new_sites.append(f_s)

    return new_sites, new_lattice
