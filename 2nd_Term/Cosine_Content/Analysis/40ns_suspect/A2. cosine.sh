#!/bin/bash

# Loop Time Length
for TL in {1..40}
do
    echo "Iteration: $TL"
    # Call your Python script with adjustable parameter
    python cosine_auto.py 40000 $((TL*1000)) 0 10
done

# Loop Time Length
for ST in {0..39}
do
    echo "Iteration: $ST"
    # Call your Python script with adjustable parameter
    python cosine_auto.py 40000 1000 $((ST*1000)) 10
done
