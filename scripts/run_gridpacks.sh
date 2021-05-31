#! /bin/bash

echo "Hello first"
echo "system here:"
cat /etc/redhat-release

function peval { echo "--> $@"; eval "$@"; }

echo "Hello World!"
peval "echo $PATH"
peval "echo $LD_LIBRARY_PATH"
peval "echo $PWD"
peval "TMPDIR=$PWD"
peval "echo $ClusterId"
peval "echo $ProcId"
peval "echo $SCRAM_ARCH"
peval "echo $CMSSW_VERSION"
peval "echo $PYTHONHOME"


echo "--> User input:"
CMSSW_MG_FOLDER=$1
JOBNAME=$2
CARDDIR=$3
GRIDPACKDIR=$4
QUEUEMODE=$5
peval "echo $CMSSW_MG_FOLDER"
peval "echo $JOBNAME"
peval "echo $CARDDIR"
peval "echo $QUEUEMODE"
echo "<-- End user input."

peval "echo $SINGULARITY_NAME"


peval "source /cvmfs/cms.cern.ch/cmsset_default.sh"

peval "cd $CMSSW_MG_FOLDER"

#create symlink to cards
peval "ln -s ${CARDDIR} link_carddir_${JOBNAME}_${ClusterId}_${ProcId}"
peval "export RELPATH_TO_CARDS=link_carddir_${JOBNAME}_${ClusterId}_${ProcId}"
peval "ls -lrth ."

peval "ls $TMPDIR"
# export PRODHOME=$CMSSW_MG_FOLDER
# TASKCMD="source gridpack_generation_modified2.sh ${JOBNAME} ${RELPATH_TO_CARDS} ${QUEUEMODE} ${TMPDIR} ALL ${SCRAM_ARCH} ${CMSSW_VERSION}"
TASKCMD="source gridpack_generation_modified.sh ${JOBNAME} ${RELPATH_TO_CARDS} ${QUEUEMODE} ${TMPDIR} ALL ${SCRAM_ARCH} ${CMSSW_VERSION}"
peval "$TASKCMD"

peval "rm ${CMSSW_MG_FOLDER}/link_carddir_${JOBNAME}_${ClusterId}_${ProcId}"

echo "--> Going to move the gridpack to storage"
peval "mv ${TMPDIR}/*${JOBNAME}*_tarball.tar.xz ${GRIDPACKDIR}"
