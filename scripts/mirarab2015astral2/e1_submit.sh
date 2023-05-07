#!/bin/bash

exit

#NTAXS=( 10 )                         # Number of taxa
#SHGHTS=( "2000000" )                 # Species tree height (generations)
#SRATES=( "0.000001" )                # Speciation rate
#NCHRS=( 500 1000 5000 10000 50000 )  # Number of characters
#REPLS=( $(seq  -f "%02g" 1 25) )     # Replicates

#NTAXS=( 50 )
#SHGHTS=( "2000000" )
#SRATES=( "0.000001" )
#NCHRS=( 500 1000 5000 10000 50000 )
#REPLS=( "01" )

NTAXS=( 50 )
SHGHTS=( "2000000" )
SRATES=( "0.000001" )
NCHRS=( 5000 )
REPLS=( $(seq  -f "%02g" 2 25) )

for NTAX in ${NTAXS[@]}; do
    for SHGHT in ${SHGHTS[@]}; do
        for SRATE in ${SRATES[@]}; do
            for NCHR in ${NCHRS[@]}; do
                MODL="model-$NTAX-$SHGHT-$SRATE-$NCHR"
                for REPL in ${REPLS[@]}; do
                    echo "Submitting $MODL $REPL..."
                    sbatch \
                        --job-name="e1.$MODL.$REPL" \
                        --output="e1.$MODL.$REPL.%j.out" \
                        --error="e1.$MODL.$REPL.%j.err" \
                        --export=MODL="$MODL",REPL="$REPL" \
                    e1_drive.sbatch
                done
            done
        done
    done
done

