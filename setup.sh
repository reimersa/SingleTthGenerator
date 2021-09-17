cd ../
export GENERATORPATH=$(readlink -f Generator)
export PYTHONPATH=$PYTHONPATH:$GENERATORPATH
# export MGDIR=$(readlink -f $GENERATORPATH/MG5_aMC_v2_8_3_2)
export EOSHOME="/eos/home-a/$USER"
export MGDIR="$EOSHOME/MG5_aMC_v2_8_3_2"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MGDIR/HEPTools/hepmc/lib
export PYTHIA8DATA=$MGDIR/HEPTools/pythia8/share/Pythia8/xmldoc

export SINGULARITY_IMAGE="$EOSHOME/slc6_latest.sif"

export SCRAM_ARCH=slc6_amd64_gcc700
# export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $HOME/CMSSW_10_2_22/src
eval `scramv1 runtime -sh`
cd $GENERATORPATH


voms-proxy-init --voms cms --valid 168:00
