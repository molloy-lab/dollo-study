#!/bin/bash

exit

sbatch \
    --job-name="atod4" \
    --output="atod4.%j.out" \
    --error="atod4.%j.err" \
    atod4_drive.sbatch

