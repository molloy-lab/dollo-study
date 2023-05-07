#!/bin/bash

exit

MODLS=( "Palaeognathae" )            # Model
NCHRS=( 500 1000 5000 10000 50000 )  # Number of characters
REPLS=( $(seq  -f "Rep%01g" 1 25) )  # Replicates

for MODL in ${MODLS[@]}; do
    for NCHR in ${NCHRS[@]}; do
        for REPL in ${REPLS[@]}; do
            echo "Submitting $MODL $NCHR $REPL..."
            sbatch \
                --job-name="b2.$MODL.$NCHR.$REPL" \
                --output="b2.$MODL.$NCHR.$REPL.%j.out" \
                --error="b2.$MODL.$NCHR.$REPL.%j.err" \
                --export=MODL="$MODL",NCHR="$NCHR",REPL="$REPL" \
            b2_drive.sbatch
        done
    done
done

