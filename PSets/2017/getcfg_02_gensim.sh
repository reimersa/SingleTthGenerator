#!/bin/bash


### DO THIS BY HAND, the CURL will fail and the cmsDriver will produce a broken PSet

export SCRAM_ARCH=slc6_amd64_gcc481

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_7_1_18/src ] ; then
  echo release CMSSW_7_1_18 already exists
else
  scram p CMSSW CMSSW_7_1_18
fi
cd CMSSW_7_1_18/src
eval `scram runtime -sh`

# Retrieve fragment from github and ensure it is there
curl  -s https://raw.githubusercontent.com/cms-sw/genproductions/071218017779916161e47643e07a49ea18433425/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py --retry 2 --create-dirs -o Configuration/GenProduction/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py
scram b
ls -lrth Configuration/GenProduction/python/ThirteenTeV

cd ../
git cms-addpkg Configuration/Generator
scram build clean
scram build
cd ..


# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_generic_LHE_pythia8_cff.py --python_filename B2G-RunIISummer15GS-00188_1_cfg.py --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:B2G-RunIISummer15GS-00188.root --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --filein "dbs:/TprimeBToTH_M-1000_RH_13TeV-madgraph/RunIIWinter15wmLHE-MCRUN2_71_V1-v1/LHE" --no_exec --mc -n 100

rm -rf CMSSW_7_1_18
