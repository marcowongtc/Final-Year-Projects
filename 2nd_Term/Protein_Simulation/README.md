# Description
This project provides crystal structure and trajectory files for the BIND peptide (AEIRLVSKDGKSKGIAYIEFK) simulation.   
The simulation involves the folding of a straightened BIND peptide in a dodecahedron box containing 0.15 M NaCl solution.   
The files included are:  
- "init.pdb": Crystal structure of BIND peptide.  
- "traj.xtc": Raw trajectory of BIND peptide.  
- "traj-align.xtc": Processed trajectory with BIND peptide aligned to the first frame.  
- "view.vmd": VMD session to view the trajectory.  

# Usage
To view the trajectory, you will need to use VMD software. 

Load the structure file prior to loading the trajectory file. For example, the command should look like:  
	```
	vmd init.pdb traj.xtc
	```

Or, an example VMD session script ("view.vmd") is provided to assist you with viewing the trajectory. The command is:  
	```
	vmd -e view.vmd
	```

