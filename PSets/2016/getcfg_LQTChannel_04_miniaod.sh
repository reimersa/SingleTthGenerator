#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc630

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_9_4_9/src ] ; then
  echo release CMSSW_9_4_9 already exists
else
  scram p CMSSW CMSSW_9_4_9
fi
cd CMSSW_9_4_9/src
eval `scram runtime -sh`

scram b
cd ../..

# cmsDriver command
cmsDriver.py  --python_filename B2G-RunIISummer16MiniAODv3-06594_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:B2G-RunIISummer16MiniAODv3-06594.root --conditions 94X_mcRun2_asymptotic_v3 --step PAT --filein file:B2G-RunIISummer16DR80Premix-05742.root --era Run2_2016,run2_miniAOD_80XLegacy --runUnscheduled --no_exec --mc -n 100

rm -rf CMSSW_9_4_9
