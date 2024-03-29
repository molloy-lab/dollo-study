#!/bin/bash

GROUPDIR="/fs/cbcb-lab/ekmolloy/group"
PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study"
PAUP="$GROUPDIR/software/paup/paup4a168_centos64"
MAKESCORENEX="$PROJDIR/tools/make_parsimony_score_nexus.py"
MAKESEARCHNEX="$PROJDIR/tools/make_parsimony_search_nexus.py"
DOLLOCDP="$PROJDIR/software/Dollo-CDP/src/dollo-cdp"

MYMODL="whales"

INOUTDIR="$PROJDIR/data/doronina2023homoplasy-bio"
if [ ! -d $INOUTDIR ]; then
    echo "$INOUTDIR does not exist!"
    exit
fi
cd $INOUTDIR

CHARS="whales_insertions.nex"
if [ ! -e $CHARS ]; then
    echo "$CHARS does not exit!"
    exit
fi
OUTGROUP="Out"

echo "Using outgroup $OUTGROUP"

MYMTHD="paup-dollo-bnb"
if [ ! -e $MYMTHD.tre ]; then
    uname -a > ${MYMTHD}_node_info.csv
    MYNODE=$( uname -a | sed 's/\./ /g' | awk '{print $2}' )

    # Build Nexus file
    python3 $MAKESEARCHNEX -i "$CHARS" \
                           -g "$OUTGROUP" \
                           -p "dollo" \
                           -b \
                           -o "./"

    echo "contree all/strict=yes treefile=$MYMTHD-strict.tre format=newick;" >> $MYMTHD.nex

    MYTIME=$(time ($PAUP -n "$MYMTHD.nex" &> $MYMTHD.log)  2>&1 1>/dev/null)

    MYSECS="$(echo $MYTIME | awk '{print $2","$4","$6}')"
    echo "$MYMODL,$MYMTHD,$MYNODE,$MYSECS" > ${MYMTHD}_runtime.csv
fi

if [ ! -e ${MYMTHD}_dollo_score.csv ]; then
    head -n1 $MYMTHD-all.trees > $MYMTHD-first.tre
    python3 $MAKESCORENEX -i "$CHARS" \
                          -t "$MYMTHD-first.tre" \
                          -p "dollo" \
                          -o "./"

    $PAUP -n "paup-dollo-score-tree-$MYMTHD-first.nex" \
        &> paup-dollo-score-tree-$MYMTHD-first.log

    MYSCORE=$(grep "Length " paup-dollo-score-tree-$MYMTHD-first.log | awk '{print $2}')
    echo "$MYMODL,$MYMTHD-first,$MYSCORE" > ${MYMTHD}-first_dollo_score.csv
fi

