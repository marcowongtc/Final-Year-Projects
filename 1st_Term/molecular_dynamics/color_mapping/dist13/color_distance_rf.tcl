
set input [open "rf-model_20-iter_13.0-dist_0.9-corr_chain1.dat" r]
while {[gets $input line] >= 0} {
    set resid [lindex $line 0]; 
    set importance [lindex $line 1]; 
    set sel [atomselect top "chain A and resid $resid"]; 
    $sel set beta $importance; 
    $sel delete
}


set input [open "rf-model_20-iter_13.0-dist_0.9-corr_chain2.dat" r]
while {[gets $input line] >= 0} {
    set resid [lindex $line 0]; 
    set importance [lindex $line 1]; 
    set sel [atomselect top "chain C and resid $resid"]; 
    $sel set beta $importance; 
    $sel delete
}