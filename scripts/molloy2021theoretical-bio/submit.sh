#!/bin/bash

exit

sbatch \
    --job-name="atod3" \
    --output="atod3.%j.out" \
    --error="atod3.%j.err" \
    atod3_drive.sbatch

