#!/bin/bash

# Loop Time Length
for TL in {1..10}
do
    echo "Iteration: $TL"
    # Call your Python script with adjustable parameter
    python PCA_protein_auto.py 10000 $((TL*1000)) 0 
done

# Loop Time Length
for ST in {0..9}
do
    echo "Iteration: $ST"
    # Call your Python script with adjustable parameter
    python PCA_protein_auto.py 10000 1000 $((ST*1000)) 
done
