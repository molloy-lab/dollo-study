#!/bin/bash

#exit

sbatch \
    --job-name="atod5" \
    --output="atod5.%j.out" \
    --error="atod5.%j.err" \
    atod5_drive.sbatch

