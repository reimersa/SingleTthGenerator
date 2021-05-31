#! /bin/bash

function peval { echo "--> $@"; eval "$@"; }

export TARGETFOLDERNAME=$1
cd $WORKDIR

peval "ls"
FILENAME=$(ls *.root)

# create sample-specific folder and all missing parent folders
echo "creating folder: $TARGETFOLDERNAME"
MKDIRCOMMAND='LD_LIBRARY_PATH='' PYTHONPATH='' gfal-mkdir -p $TARGETFOLDERNAME; sleep 10s;'
peval "$MKDIRCOMMAND"

# copy the file from /scratch to T2
echo "copying file $FILENAME"
peval "LD_LIBRARY_PATH='' PYTHONPATH='' gfal-copy -f file:////$PWD/$FILENAME $TARGETFOLDERNAME"
echo "removing file $FILENAME in $PWD"
peval "rm $FILENAME"
