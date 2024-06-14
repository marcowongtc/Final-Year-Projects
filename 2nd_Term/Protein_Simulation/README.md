# Description
This project provides crystal structure and trajectory files for the BIND peptide (AEIRLVSKDGKSKGIAYIEFK) simulation.   
The simulation involves the folding of a straightened BIND peptide in a dodecahedron box containing 0.15 M NaCl solution.   
The files included are:  
- "init.pdb": Crystal structure of BIND peptide.  
- "traj.xtc": Raw trajectory of BIND peptide.  
- "traj-align.xtc": Processed trajectory with BIND peptide aligned to the first frame.  
- "view.vmd": VMD session to view the trajectory.  



# GROMACS | Run MD Simulation 

To run a GROMACS simulation, you will need the following files:

1. **gro**: The coordinate file (.gro format) containing the initial structure of your system.
2. **mdp**: The input file (.mdp format) specifying the simulation parameters, such as integrator, time step, temperature, etc.
3. **top**: The topology file (.top format) describing the molecular topology of your system.
4. **ff**: The force field files (.itp or .ff format) defining the force field parameters for the atoms in your system.

Assuming you have GROMACS installed and configured correctly, you can run a GROMACS simulation using the following steps:

1. Create a working directory and navigate to it:
    
    ```bash
    mkdir my_simulation
    cd my_simulation
    
    ```
    
2. Copy the necessary files (gro, mdp, top, ff) to the working directory.
	```bash
	# mdp example | [simulation_time = 2ns, sampling_time_step = 0.1ps]
	# Run Control Parameters
	integrator              = md                # leap-frog integrator
	tinit                   = 0
	dt                      = 0.002             # integrator step: 0.002fs 
	nsteps                  = 1000000           
	# number of steps: 10^6, Total Time Length: 0.002fs*10^6=2ns                     

	# Output frequency
	nstxout                 = 0                 # do not output coordinates (x)
	nstvout                 = 0                 # do not output velocities (v)
	nstfout                 = 0                 # do not output force (f)
	nstlog                  = 50                # update log file every 0.1 ps
	nstenergy               = 50                # save energies every 0.1 ps
	nstxout-compressed      = 50                # compressed trajectory file every 0.1 ps (.xtc file) 
	
	...

	```

    
3. Perform the production simulation:
    
    ```bash
	# Perform in CPU
    gmx grompp -f md.mdp -c em.gro -p system.top -o md.tpr
    gmx mdrun -v -deffnm md
    ```
    
    Replace `md.mdp` with the appropriate name of your production simulation .mdp file and `em.gro` with the name of the minimized structure .gro file.

	```bash
	# Perform in GPU
	nvidia-smi # check GPU Usage in server

	gmx grompp -f md.mdp -c em.gro -p system.top -o md.tpr
    gmx mdrun -v -deffnm '[jobname]' -ntomp 8 -gpu_id '[gpu_id]' -pin on -pinstride 1 -pinoffset '[8*gpu_id]' -nb gpu -bonded gpu -pme gpu -pmefft gpu -update gpu
    
    ```	

	To drop specific computing tasks on gpu, please ensure to explicitly add the appropriate flags (-nb: non-bonded interactions, -bonded: bonded interactions, etc. Please refer to the [GROMACS user guide](https://manual.gromacs.org/2022/onlinehelp/gmx-mdrun.html)) to the command. In the case of the GPU1 server, which has 24 cpu threads and 4 available gpus with id 0, 1, 2, and 3, it is generally recommended to assign 8 threads (-ntomp) and 1 gpu (specify gpu_id) for each job to achieve optimal performance. 
    

These commands use `gmx grompp` to prepare the input files and `gmx mdrun` to perform the simulation. The `-deffnm` flag specifies the base name for output files, and the `-v` flag enables verbose output.

Make sure to adjust the file names and paths in the commands based on your specific file names and directory structure.

Please note that running GROMACS simulations may require additional steps, such as equilibration and analysis, depending on your specific objectives. The above steps provide a basic outline for running a simulation, but you might need to customize the protocol further for your specific needs.


# GROMACS | Trajectory Recentering



```bash

gmx trjconv -s md.tpr -f md.xtc -o md_allign.xtc -pbc mol -center

```

Select 1 ("Protein") as the group to be centered and 0 ("System") for output.



# VMD | Trajectory and Structure Visualization
To view the trajectory, you will need to use VMD software. 

Load the structure file prior to loading the trajectory file. For example, the command should look like:  
	```
	vmd init.pdb traj.xtc
	```

Or, an example VMD session script ("view.vmd") is provided to assist you with viewing the trajectory. The command is:  
	```
	vmd -e view.vmd
	```