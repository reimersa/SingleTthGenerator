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
cmsDriver.py  --python_filename B2G-RunIIAutumn18NanoAODv7-02794_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:B2G-RunIIAutumn18NanoAODv7-02794.root --conditions 102X_upgrade2018_realistic_v21 --step NANO --filein "dbs:/TprimeBToTH_TLep_Hbb_LH_MT1000_MH100_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM" --era Run2_2018,run2_nanoAOD_102Xv1 --no_exec --mc -n 100

rm -rf CMSSW_10_2_24_patch1
