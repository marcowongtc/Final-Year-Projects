# Principal Component Analysis on Molecular Dynamics of Protein and N-Dimensional Random Walkers in Different Time Scale

## I | Overview

![overivew](/Asset/2nd_Term/overview.png)



### 1 | MD Simulation of Simple Peptide

#### Simulation Information

![Simulation box](/Asset/2nd_Term/solvent%20peptide.png)

Structure: Peptide with 21 residues  
ALA-GLU-ILE-ARG-LEU-VAL-SER-LYS-ASP-GLY-LYS-SER-LYS-GLY-ILE-ALA-TYR-ILE-GLU-PHE-LYS

Solvent: Water Molecules  
Coordinate trajectory selection: 21 𝐶−𝛼, 3 dimension (63-D)  




#### Simulation Trajectory 

| [1𝑝𝑠,1𝑓𝑠]   | [1𝑛𝑠, 0.1𝑝𝑠]   | [10𝑛𝑠, 1𝑝𝑠]  |
| ----------- | ----------- | -----------|
| ![Example](/Asset/2nd_Term/fs.gif)      | ![Example](/Asset/2nd_Term/ps_1ns.gif)       | ![Example](/Asset/2nd_Term/ps_10ns.gif)      |

[Simulation Time, time of each steps]

Calculation Software: `GROMACS`  
Visualization: `VMD` 


#### Analysis of Cosine Content in Different Time Scale 
![time tuning](/Asset/2nd_Term/MD_time_tuning.png)



### 2 | Random Diffusion Simulation


#### Simulation Information

![random diffusion simulation](/Asset/2nd_Term/random_walker.png)

Random Walker (63-D)  
Equal Probability to go forward / backward for each step  

#### Analysis

![random tuning](/Asset/2nd_Term/random_tuning.png)




## II | Code Recipe

### Simulation: [Peptide](./Protein_Simulation/README.md) + [Random diffusion](./Diffustion_Simulation/README.md)
### Analysis: [Principal Component Analysis (PCA)](./PCA/README.md) + [Cosine Content](./Cosine_Content/README.md)

## III | Result 

### [2nd Term FYP Report](https://drive.google.com/file/d/1Ypya1y-LJNdiyEQsA5PrQoYCWyfY4GnQ/view?usp=sharing)
### [2nd Term FYP Presentation](https://docs.google.com/presentation/d/1DTLwQxJXGX2oSiw0lCECjONuZutY6F_y/edit?usp=sharing&ouid=110148678779983739038&rtpof=true&sd=true)

### Figure: [PCA Plot](https://shaded-cannon-4d7.notion.site/Protein-PCA-and-plot-nanosecond-8a5c0c3d766c42298112c5debfc02380?pvs=4) + [Cosine Content Overview](https://shaded-cannon-4d7.notion.site/Cosine-content-Analysis-c3c2dbd010cd48228e208fa464f38570?pvs=4) + [Cosine Content in Different Time Scale](https://shaded-cannon-4d7.notion.site/Cosine-Content-Final-1e6228d275df49e183f33dd41720c048?pvs=4)