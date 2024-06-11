
mol load pdb structure-GC.pdb
set input [open "chain_A_importance_lr.dat" r]
while {[gets $input line] >= 0} {
    set resid [lindex $line 0]; 
    set importance [lindex $line 1]; 
    set sel [atomselect top "resid $resid"]; 
    $sel set beta $importance; 
    $sel delete
}

