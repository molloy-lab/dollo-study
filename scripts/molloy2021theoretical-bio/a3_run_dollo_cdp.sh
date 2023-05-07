#!/bin/bash

GROUPDIR="/fs/cbcb-lab/ekmolloy/group"
PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study"
PAUP="$GROUPDIR/software/paup/paup4a168_centos64"
MAKESCORENEX="$PROJDIR/tools/make_parsimony_score_nexus.py"
MAKESEARCHNEX="$PROJDIR/tools/make_parsimony_search_nexus.py"
DOLLOCDP="$PROJDIR/software/Dollo-CDP/src/dollo-cdp"

MYMODL="palaeognathae"

INOUTDIR="$PROJDIR/data/molloy2021theoretical-bio"
if [ ! -d $INOUTDIR ]; then
    echo "$INOUTDIR does not exist!"
    exit
fi
cd $INOUTDIR

CHARS="palaeognathae.nex"
if [ ! -e $CHARS ]; then
    echo "$CHARS does not exit!"
    exit
fi
OUTGROUP="galGal"

echo "Using outgroup $OUTGROUP"

MYMTHD="dollo-cdp"
if [ ! -e $MYMTHD.tre ]; then
    uname -a > ${MYMTHD}_node_info.csv
    MYNODE=$( uname -a | sed 's/\./ /g' | awk '{print $2}' )
    
    MYTIME=$(time ($DOLLOCDP -i $CHARS \
                             -g $OUTGROUP \
                             -o $MYMTHD.tre &> $MYMTHD.log) 2>&1 1>/dev/null)

    MYSECS="$(echo $MYTIME | awk '{print $2","$4","$6}')"
    echo "$MYMODL,$MYMTHD,$MYNODE,$MYSECS" > ${MYMTHD}_runtime.csv
fi

if [ ! -e ${MYMTHD}_dollo_score.csv ]; then
    python3 $MAKESCORENEX -i "$CHARS" \
                          -t "$MYMTHD.tre" \
                          -p "dollo" \
                          -o "./"

    $PAUP -n "paup-dollo-score-tree-$MYMTHD.nex" \
        &> paup-dollo-score-tree-$MYMTHD.log

    MYSCORE=$(grep "Length " paup-dollo-score-tree-$MYMTHD.log | awk '{print $2}')
    echo "$MYMODL,$MYMTHD,$MYSCORE" > ${MYMTHD}_dollo_score.csv
fi


