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
cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-03915_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIIAutumn18DRPremix-03915.root --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --filein file:B2G-RunIIAutumn18DRPremix-03915_0.root --era Run2_2018 --runUnscheduled --no_exec --mc -n 100

rm -rf CMSSW_10_2_26_patch1
