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
cmsDriver.py  --python_filename B2G-RunIIAutumn18DRPremix-03915_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIIAutumn18DRPremix-03915_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW" --conditions 102X_upgrade2018_realistic_v15 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --geometry DB:Extended --filein file:B2G-RunIIFall18wmLHEGS-03837.root --datamix PreMix --era Run2_2018 --no_exec --mc -n 123

rm -rf CMSSW_10_2_26_patch1
