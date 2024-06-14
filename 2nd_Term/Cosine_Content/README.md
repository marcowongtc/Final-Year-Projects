# Overview of Program for Analysis

```bash
.
|   # analysis
├── 1. slice.py                # Slicing of trajectory for varying time length
├── 2. PCA_protein_auto.py     # PCA
├── 3. cosine_auto.py          # cosine content
|
|   # plotting
├── P1. PCA_plotting_auto.py        
├── P2. cosine_PCtrend_plotting.py
├── P3. cosine_TL_ST_plotting.py
|
|   # repeat the program above (can change with different parameters)
├── A1. PCA.sh
├── A2. cosine.sh
└── A3. PCA_plot.sh
```


# Principal Component Analysis (PCA) ([program](./Updated_Program/2.%20PCA_protein_auto.py))

Method of finding new basis of trajectory, which the projections on the new basis are uncorrelated with each other. We call the new basis as principal mode (PC) / motion mode of trajectory. The projection with largest variance is called PC1, which is the main analyzing candidate in the project.

The whole technique is introduced in detail in the Section: Principal Component Analysis of [Presentation](https://docs.google.com/presentation/d/1DTLwQxJXGX2oSiw0lCECjONuZutY6F_y/edit?usp=sharing&ouid=110148678779983739038&rtpof=true&sd=true) and [Report](https://drive.google.com/file/d/1Ypya1y-LJNdiyEQsA5PrQoYCWyfY4GnQ/view?usp=sharing).

The program is developed using `Python`. Here is the workflow.

1. calculate the covariance matrix of the given trajectory  
$$C_{ij}= \left< (x_i(t)-\left< x_i(t) \right> )(x_j(t)- \left< x_j(t) \right> \right>$$

2. manipulate the eigenvectors (new basis) $R$ and eigenvalues (new variance) $\vec{\lambda}$ of the covariance matrix using in-built function in `numpy.linalg.eig` 

3. transform the trajectory under original basis into new basis , or in other words, calculate the projection of trajectory on new basis by using eigenvector matrix $R$.     
    $$\vec{p}(t)=R^T(\vec{x}(t)-\left<\vec{x}(t)\right>)$$

4. PC is plotted for analysis using `matplolib` and trajectory data `.npy` in new basis is outputted for further analysis 


# Cosine Content Analysis ([program](./Updated_Program/3.%20cosine_auto.py))

Method of measuring the cosine content in PCs   
$$c_n = \frac{2}{T}\left(\int^{T}_0cos(\frac{n\pi t}{T})p_n(t)\right)^2\left(\int^{T}_0p^2_n(t)dt\right)^{-1}$$

$0$ represents no cosine and $1$ represents a perfect cosine

The program is developed using `Python`. The integration part used `scipy.integrate` package. 

the standard deviation of cosine content $\delta$ is found by calculating the cosine content of slices of trajectory of same time length. The number of slice varies as the time of slice varies for slicing the same trajectory. It is discussed visually in [Here (Peptide)](https://github.com/marcowongtc/FYP/blob/main/2nd_Term/README.md#analysis-of-cosine-content-in-different-time-scale) and [Here (Random Diffusion)](https://github.com/marcowongtc/FYP/blob/main/2nd_Term/README.md#analysis-of-cosine-content-in-different-time-scale).

