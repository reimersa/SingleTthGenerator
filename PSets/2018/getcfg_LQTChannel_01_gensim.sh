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

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIFall18wmLHEGS-03837 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-03837-fragment.py
scram b
cd ../..

# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall18wmLHEGS-03837-fragment.py --python_filename B2G-RunIIFall18wmLHEGS-03837_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall18wmLHEGS-03837.root --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 100

rm -rf CMSSW_10_2_26_patch1
