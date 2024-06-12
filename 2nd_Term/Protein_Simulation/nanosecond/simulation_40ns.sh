gmx grompp -f PROD_40ns.mdp -c eq_npt.gro -p topol.top -o 40ns_1ps.tpr
gmx mdrun -v -deffnm 40ns_1ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 

