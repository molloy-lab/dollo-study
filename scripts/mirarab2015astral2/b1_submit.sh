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
                MODL="model.$NTAX.$SHGHT.$SRATE"
                for REPL in ${REPLS[@]}; do
                    echo "Submitting $MODL $NCHR $REPL..."
                    sbatch \
                        --job-name="b1.$MODL.$NCHR.$REPL" \
                        --output="b1.$MODL.$NCHR.$REPL.%j.out" \
                        --error="b1.$MODL.$NCHR.$REPL.%j.err" \
                        --export=NTAX="$NTAX",SHGHT="$SHGHT",SRATE="$SRATE",NCHR="$NCHR",REPL="$REPL" \
                    b1_drive.sbatch
                done
            done
        done
    done
done

