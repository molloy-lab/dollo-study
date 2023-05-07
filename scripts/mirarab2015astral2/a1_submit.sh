#!/bin/bash

#exit

NTAXS=( 10 50 100 200 )              # Number of taxa
SHGHTS=( "2000000" )                 # Species tree height (generations)
SRATES=( "0.000001" )                # Speciation rate
REPLS=( $(seq  -f "%02g" 1 25) )     # Replicates

for NTAX in ${NTAXS[@]}; do
    for SHGHT in ${SHGHTS[@]}; do
        for SRATE in ${SRATES[@]}; do
            MODL="model.$NTAX.$SHGHT.$SRATE"
            for REPL in ${REPLS[@]}; do
                echo "Submitting $MODL $REPL..."
                sbatch \
                    --job-name="a1.$MODL.$REPL" \
                    --output="a1.$MODL.$REPL.%j.out" \
                    --error="a1.$MODL.$REPL.%j.err" \
                    --export=NTAX="$NTAX",SHGHT="$SHGHT",SRATE="$SRATE",REPL="$REPL" \
                a1_drive.sbatch
            done
        done
    done
done

