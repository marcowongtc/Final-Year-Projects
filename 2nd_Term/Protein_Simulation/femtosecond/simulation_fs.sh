gmx grompp -f PROD_fs.mdp -c eq_npt.gro -p topol.top -o 1000fs_1.tpr
gmx mdrun -v -deffnm 1000fs_1 -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 

gmx grompp -f PROD_fs.mdp -c eq_npt.gro -p topol.top -o 1000fs_2.tpr
gmx mdrun -v -deffnm 1000fs_2 -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 

gmx grompp -f PROD_fs.mdp -c eq_npt.gro -p topol.top -o 1000fs_3.tpr
gmx mdrun -v -deffnm 1000fs_3 -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 

gmx trjconv -s 1000fs_1.tpr -f 1000fs_1.xtc -o 1000fs_1_center.xtc -pbc mol -center
gmx trjconv -s 1000fs_2.tpr -f 1000fs_2.xtc -o 1000fs_2_center.xtc -pbc mol -center
gmx trjconv -s 1000fs_3.tpr -f 1000fs_3.xtc -o 1000fs_3_center.xtc -pbc mol -center