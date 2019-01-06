#!/bin/bash
#PBS -l nodes=1:ppn=20
#PBS -l walltime=00:30:00
#PBS -q debug
#PBS -N au_lj_vacancy_40

cd $PBS_O_WORKDIR
/home/azadoks/.local/bin/gulp <\
    /home/azadoks/git/3-320/lab1/2a/au_lj_vacancy_40.in >\
    /home/azadoks/git/3-320/lab1/2a/au_lj_vacancy_40.out
