#!/bin/bash

MYMODL=$1
INOUTDIR=$2

PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study"
PAUP="/fs/cbcb-lab/ekmolloy/group/software/paup/paup4a168_centos64"
MAKESCORENEX="$PROJDIR/tools/make_parsimony_score_nexus.py"
MAKESEARCHNEX="$PROJDIR/tools/make_parsimony_search_nexus.py"
DOLLOCDP="$PROJDIR/software/Dollo-CDP/src/dollo-cdp"
COMPARE="$PROJDIR/tools/compare_two_trees.py"

cd $INOUTDIR
CHARS="mschars.nex"
if [ ! -e $CHARS ]; then
    echo "$CHARS does not exit!"
    exit
fi
OUTGROUP="0"

echo "Using outgroup $OUTGROUP"

# Run fast heuristic search

MYMTHD="paup-dollo-fast-hsearch"
if [ ! -e $MYMTHD-all.trees ]; then
    uname -a > ${MYMTHD}_node_info.csv
    MYNODE=$( uname -a | sed 's/\./ /g' | awk '{print $2}' )

    # Build Nexus file
    python3 $MAKESEARCHNEX -i "$CHARS" \
                           -g "$OUTGROUP" \
                           -p "dollo" \
                           -f \
                           -o "./"

    MYTIME=$(time ($PAUP -n "$MYMTHD.nex" &> $MYMTHD.log)  2>&1 1>/dev/null)

    MYSECS="$(echo $MYTIME | awk '{print $2","$4","$6}')"
    echo "$MYMODL,$MYMTHD,$MYNODE,$MYSECS" > ${MYMTHD}_runtime.csv
fi

if [ ! -e ${MYMTHD}-first_dollo_score.csv ]; then
    # Build Nexus file
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


# Run dollo-cdp

TREES="$MYMTHD-all.trees"
MYMTHD="dollo-cdp-fast"
if [ ! -e $MYMTHD.tre ]; then
    uname -a > ${MYMTHD}_node_info.csv
    MYNODE=$( uname -a | sed 's/\./ /g' | awk '{print $2}' )

    MYTIME=$(time ($DOLLOCDP -i $CHARS \
                             -g $OUTGROUP \
                             -t $TREES \
                             -o $MYMTHD.tre &> $MYMTHD.log) 2>&1 1>/dev/null)

    MYSECS="$(echo $MYTIME | awk '{print $2","$4","$6}')"
    echo "$MYMODL,$MYMTHD,$MYNODE,$MYSECS" > ${MYMTHD}_runtime.csv
fi

if [ ! -e ${MYMTHD}_dollo_score.csv ]; then
    # Build Nexus file
    python3 $MAKESCORENEX -i "$CHARS" \
                          -t "$MYMTHD.tre" \
                          -p "dollo" \
                          -o "./"

    $PAUP -n "paup-dollo-score-tree-$MYMTHD.nex" \
        &> paup-dollo-score-tree-$MYMTHD.log

    MYSCORE=$(grep "Length " paup-dollo-score-tree-$MYMTHD.log | awk '{print $2}')
    echo "$MYMODL,$MYMTHD,$MYSCORE" > ${MYMTHD}_dollo_score.csv
fi

