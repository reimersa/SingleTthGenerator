#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_24_patch1/src ] ; then
  echo release CMSSW_10_2_24_patch1 already exists
else
  scram p CMSSW CMSSW_10_2_24_patch1
fi
cd CMSSW_10_2_24_patch1/src
eval `scram runtime -sh`

scram b
cd ../..


# cmsDriver command
cmsDriver.py  --python_filename B2G-RunIISummer16NanoAODv7-03872_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIISummer16NanoAODv7-03872.root --conditions 102X_mcRun2_asymptotic_v8 --step NANO --filein "dbs:/TprimeBToTH_TLep_Hbb_LH_MT1000_MH100_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM" --era Run2_2016,run2_nanoAOD_94X2016 --no_exec --mc -n 100

rm -rf CMSSW_10_2_24_patch1
