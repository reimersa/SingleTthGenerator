#! /bin/bash
echo "hello from submit_cmsRun_command.sh"

function peval { echo "--> $@"; eval "$@"; }

peval "echo $PATH"
peval "echo $LD_LIBRARY_PATH"
peval "echo $PWD"
# peval "export WORKDIR=$PWD"
peval "echo $ClusterId"
peval "echo $ProcId"
peval "echo $SCRAM_ARCH"
peval "echo $CMSSW_VERSION"

#Pick up arguments
CODEFOLDER=$1       # ......./SingleTth/Generator
ARCHTAG=$2
CMSSWDIR=$3         # Location of CMSSW for this production
JOBLIST=$4          # List of cmsRun commands


#Set up CMSSW and PYTHONPATH
peval "source /cvmfs/cms.cern.ch/cmsset_default.sh"
peval "export SCRAM_ARCH=$ARCHTAG"
peval "cd $CMSSWDIR/src"
peval `scramv1 runtime -sh`

# to include python modules in basefolder and PSet folder
export PYTHONPATH=$PYTHONPATH:$CODEFOLDER
# export PYTHONPATH=$CODEFOLDER/PSets:$PYTHONPATH
echo $PYTHONPATH

# each worker node has local /scratch space to be used during job run. This is where the output of cmsRun will end up in.
# export WORKDIR=$PWD
peval "cd $WORKDIR"
echo WORKDIR: $WORKDIR

echo $LD_LIBRARY_PATH
echo $PATH
echo $PYTHONPATH

# the joblist contains a list of 'cmsRun pSet.py ......' commands
TASKCMD=$(cat $JOBLIST | sed "$((ProcId + 1))q;d")
peval "echo TASKCMD is: $TASKCMD"
TASK_FAILED=0
eval $TASKCMD || { echo "cmsRun failed. Going to delete rootfile(s)." ; rm -rf $(ls *.root) ; }



peval "echo Done."
