#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc630

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_9_3_6/src ] ; then
  echo release CMSSW_9_3_6 already exists
else
  scram p CMSSW CMSSW_9_3_6
fi
cd CMSSW_9_3_6/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIFall17wmLHEGS-00341 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIFall17wmLHEGS-00341-fragment.py
scram b
cd ../..

SEED=$(($(date +%s) % 100 + 1))


# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIFall17wmLHEGS-00341-fragment.py --python_filename B2G-RunIIFall17wmLHEGS-00341_1_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIIFall17wmLHEGS-00341.root --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})"\\nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2017 --no_exec --mc -n 100

rm -rf CMSSW_9_3_6
