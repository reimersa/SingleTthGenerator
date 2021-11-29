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
cmsDriver.py  --python_filename B2G-RunIISummer16DR80Premix-05742_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIISummer16DR80Premix-05742_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --filein file:B2G-RunIISummer15wmLHEGS-05559.root --datamix PreMix --era Run2_2016 --no_exec --mc -n 123

rm -rf CMSSW_8_0_31
