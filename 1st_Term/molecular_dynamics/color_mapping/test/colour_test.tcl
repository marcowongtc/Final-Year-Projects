set input [open "chain_A_importance_lr.dat" r]
while {[gets $input line] >= 0} {
    set resid [lindex $line 0]; 
    set importance [lindex $line 1]; 
    set sel [atomselect top "chain A and resid $resid"]; 
    $sel set beta $importance; 
    $sel delete
}

set input [open "chain_C_importance_lr.dat" r]
while {[gets $input line] >= 0} {
    set resid [lindex $line 0]; 
    set importance [lindex $line 1]; 
    set sel [atomselect top "chain C and resid $resid"]; 
    $sel set beta $importance; 
    $sel delete
}


