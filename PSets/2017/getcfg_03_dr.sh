#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc530

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_8_0_21/src ] ; then
  echo release CMSSW_8_0_21 already exists
else
  scram p CMSSW CMSSW_8_0_21
fi
cd CMSSW_8_0_21/src
eval `scram runtime -sh`

scram b
cd ../..

# cmsDriver command
cmsDriver.py  --python_filename B2G-RunIISummer16DR80Premix-00632_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:B2G-RunIISummer16DR80Premix-00632_0.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --filein "dbs:/TprimeBToTH_M-1000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer15GS-MCRUN2_71_V1-v1/GEN-SIM" --datamix PreMix --era Run2_2016 --no_exec --mc -n 100

rm -rf CMSSW_8_0_21
