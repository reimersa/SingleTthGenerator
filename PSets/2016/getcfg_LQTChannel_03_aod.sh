#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc530

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_8_0_31/src ] ; then
  echo release CMSSW_8_0_31 already exists
else
  scram p CMSSW CMSSW_8_0_31
fi
cd CMSSW_8_0_31/src
eval `scram runtime -sh`

scram b
cd ../..


# cmsDriver command
cmsDriver.py  --python_filename B2G-RunIISummer16DR80Premix-05742_2_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:B2G-RunIISummer16DR80Premix-05742.root --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --filein file:B2G-RunIISummer16DR80Premix-05742_0.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 100

rm -rf CMSSW_8_0_31
