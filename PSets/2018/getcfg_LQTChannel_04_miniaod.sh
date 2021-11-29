#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_26_patch1/src ] ; then
  echo release CMSSW_10_2_26_patch1 already exists
else
  scram p CMSSW CMSSW_10_2_26_patch1
fi
cd CMSSW_10_2_26_patch1/src
eval `scram runtime -sh`

scram b
cd ../..

# cmsDriver command
cmsDriver.py  --python_filename B2G-RunIIAutumn18MiniAOD-03914_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIIAutumn18MiniAOD-03914.root --conditions 102X_upgrade2018_realistic_v15 --step PAT --geometry DB:Extended --filein file:B2G-RunIIAutumn18DRPremix-03915.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 100

rm -rf CMSSW_10_2_26_patch1
