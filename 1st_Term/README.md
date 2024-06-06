# Machine Learning Importance-Residue Profile Analysis on MD simulation of NF-κB p52 homodimer-DNA complexes

### Molecular Dynamics 
> 12 $\mu s$ Trajectories of PSel-κB p52 Homodimer-DNA Complex Simulations 
>   - Natural G/C centric DNA
>   - -1/+1 swap DNA (1 base pair change)
> 
> Simulation Software: `GROMACS`   
> Visualization Software: `Visual Molecular Dynamics (VMD)`
>

***

### Machine Learning 

> Machine Learning Model 
> - ***Logistic Regression*** (LR)
> - ***Random Forest*** (RF)
>
> Hyperparameter Tuning
> - Correlation Cutoff $\rho$
> - Distance Cutoff $d$
> - Iteration Cutoff $n$
> - Partition Ratio $p$
>
> Language: `Matlab`  
> Program:  
>> Grasping the **dynamical importance profile** of all residues in p52 homodimer  to differentiate two different complex reaction, in turn obtaining **important residues of p52 homodimer** and its **dynamical behavior** under hyperparameter tuning to the reaction when there is a subtle change in DNA  
> 
> 

***

### Importance Profile Mapping to Structure 

> Language: `VMD Tk Console`  
> Program: 
>> Importing importance profile which maps with `resID` (residue id), then map the importance as gradient of color 

***

### Dynamics of Important Profile 

> Language: `Python` - `Matplotlib` & `Numpy`   
> Program:   
>> Plotting selected important residue (manually picked from observing importance profile) then plotting its trend of varying hyperparameter.   
>>
>> The results are categorized into
>> - increasing
>> - decreasing
>> - generally unchanged

