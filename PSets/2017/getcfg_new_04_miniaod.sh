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
cmsDriver.py  --python_filename B2G-RunIIFall17MiniAODv2-00424_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIFall17MiniAODv2-00424.root --conditions 94X_mc2017_realistic_v14 --step PAT --scenario pp --filein "dbs:/TprimeBToTH_M-1000_LH_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17DRPremix-PU2017_94X_mc2017_realistic_v11-v1/AODSIM" --era Run2_2017,run2_miniAOD_94XFall17 --runUnscheduled --no_exec --mc -n 123

rm -rf CMSSW_9_4_7
