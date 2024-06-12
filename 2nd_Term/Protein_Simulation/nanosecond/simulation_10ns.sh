gmx grompp -f PROD_10ns.mdp -c eq_npt.gro -p topol.top -o 10ns_10ps.tpr
gmx mdrun -v -deffnm 10ns_10ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 

