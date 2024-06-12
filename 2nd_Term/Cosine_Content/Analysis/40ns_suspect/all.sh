#!/bin/bash
"""
# slice.py
#---------------------
python 1.\ slice.py 44038ps_1ps

# PCA.sh
#----------------------
# Loop Time Length
for TL in {1..40}
do
    echo "Iteration: $TL"
    # Call your Python script with adjustable parameter
    python 2.\ PCA_protein_auto.py 40000 $((TL*1000)) 0 
done

# Loop Time Length
for ST in {0..39}
do
    echo "Iteration: $ST"
    # Call your Python script with adjustable parameter
    python 2.\ PCA_protein_auto.py 40000 1000 $((ST*1000)) 
done





# PCA_plot.sh
# ---------------------------------
# Loop Time Length
for TL in {1..40}
do
    echo "Iteration: $TL"
    # Call your Python script with adjustable parameter
    python P1.\ PCA_plotting_auto.py 40000 $((TL*1000)) 0 5
done

# Loop Time Length
for ST in {0..39}
do
    echo "Iteration: $ST"
    # Call your Python script with adjustable parameter
    python P1.\ PCA_plotting_auto.py 40000 1000 $((ST*1000)) 5
done
"""

# cosine.sh
#-----------------------
# Loop Time Length
for TL in {1..40}
do
    echo "Iteration: $TL"
    # Call your Python script with adjustable parameter
    python 3.\ cosine_auto.py 40000 $((TL*1000)) 0 10
done

# Loop Start Time
for ST in {0..39}
do
    echo "Iteration: $ST"
    # Call your Python script with adjustable parameter
    python 3.\ cosine_auto.py 40000 1000 $((ST*1000)) 10
done


# P2. cosine_PCtrend_plotting
#--------------------------------
python P2.\ cosine_PCtrend_plotting.py 40000 1000 1000 10 5

# P3. cosine_TL_ST_plotting
#--------------------------------
python P3.\ cosine_TL_ST_plotting.py 40000 1000 1000 10 5