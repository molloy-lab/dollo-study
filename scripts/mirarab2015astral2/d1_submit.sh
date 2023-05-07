#!/bin/bash

exit

NTAXS=( 10 50 100 200 )              # Number of taxa
SHGHTS=( "2000000" )                 # Species tree height (generations)
SRATES=( "0.000001" )                # Speciation rate
NCHRS=( 500 1000 5000 10000 50000 )  # Number of characters
REPLS=( $(seq  -f "%02g" 1 25) )     # Replicates

for NTAX in ${NTAXS[@]}; do
    for SHGHT in ${SHGHTS[@]}; do
        for SRATE in ${SRATES[@]}; do
            for NCHR in ${NCHRS[@]}; do
                MODL="model-$NTAX-$SHGHT-$SRATE-$NCHR"
                for REPL in ${REPLS[@]}; do
                    echo "Submitting $MODL $REPL..."
                    sbatch \
                        --job-name="d1.$MODL.$REPL" \
                        --output="d1.$MODL.$REPL.%j.out" \
                        --error="d1.$MODL.$REPL.%j.err" \
                        --export=MODL="$MODL",REPL="$REPL" \
                    d1_drive.sbatch
                done
            done
        done
    done
done

