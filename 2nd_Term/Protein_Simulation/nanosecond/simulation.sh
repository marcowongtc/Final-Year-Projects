gmx grompp -f PROD_10ns.mdp -c eq_npt.gro -p topol.top -o 10ns_0.1ps.tpr
gmx mdrun -v -deffnm 10ns_0.1ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 


gmx grompp -f PROD_20ns.mdp -c eq_npt.gro -p topol.top -o 20ns_0.1ps.tpr
gmx mdrun -v -deffnm 20ns_0.1ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 


gmx grompp -f PROD_30ns.mdp -c eq_npt.gro -p topol.top -o 30ns_0.1ps.tpr
gmx mdrun -v -deffnm 30ns_0.1ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 


gmx grompp -f PROD_40ns.mdp -c eq_npt.gro -p topol.top -o 40ns_0.1ps.tpr
gmx mdrun -v -deffnm 40ns_0.1ps -ntomp 8 -gpu_id 0 -pin on -pinstride 1 -pinoffset 0 -nb gpu -bonded gpu -pme gpu -pmefft gpu 
