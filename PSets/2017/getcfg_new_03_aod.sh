#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc630

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_9_4_7/src ] ; then
  echo release CMSSW_9_4_7 already exists
else
  scram p CMSSW CMSSW_9_4_7
fi
cd CMSSW_9_4_7/src
eval `scram runtime -sh`

scram b
cd ../..

# cmsDriver command
cmsDriver.py step1 --fileout file:outfile.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v14 --step RAW2DIGI,L1Reco,RECO,RECOSIM --filein file:infile --geometry DB:Extended  --era Run2_2017,run2_miniAOD_94XFall17 --python_filename pset_new_03_aod.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 123

rm -rf CMSSW_9_4_7
