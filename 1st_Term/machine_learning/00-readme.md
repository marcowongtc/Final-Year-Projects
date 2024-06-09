## Machine Training Procedure

1. Do the VMD tutorial and use VMD to view the trajectories. A premade session to view the trajectory could be loaded as:
	``` bash
	vmd -e view.vmd
	```

2. Use `GROMACS` to measure the minimum distance between each residue of p52 dimer and each nucleobase of the central DNA (Position -5 to +5). This `index.ndx` is needed for telling `GROMACS` which part to calculate. The measurement could be done as:
	``` bash
	gmx pairdist -f traj.xtc -s structure.pdb -n index.ndx -o mindisres.xvg -refgrouping res -selgrouping res
	```
	Choose Protein as the reference and Central_DNA as the selection when prompt. 
	Since we have 295 residues in each chain of p52 dimer (the index order is residue 35 to 329 of chain A [chain I], then residue 35 to 329 of chain C [chain II] ) and 11 nucleobases in each strand of central DNA (the position order is +5 to -5 of chain B[strand 3'], then -5 to +5 of chain D[strand 5']), the obtained `mindisres.xvg` contains 295*2*11*2 columns. The columns contain distance like this: pro1-dna1, pro2-dna1, ..., pro1-dna2, pro2-dna2, ...

3. Use `mindisres.xvg` as the training set and train your own linear logistic regression and random forest model in `ml.m`. 
