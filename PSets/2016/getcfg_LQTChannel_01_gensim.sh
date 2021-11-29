#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc481

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_7_1_47/src ] ; then
  echo release CMSSW_7_1_47 already exists
else
  scram p CMSSW CMSSW_7_1_47
fi
cd CMSSW_7_1_47/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIISummer15wmLHEGS-05559 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-05559-fragment.py
scram b
cd ../..

# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-05559-fragment.py --python_filename B2G-RunIISummer15wmLHEGS-05559_1_cfg.py --eventcontent RAWSIM,LHE --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIISummer15wmLHEGS-05559.root --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --magField 38T_PostLS1 --no_exec --mc -n 100

rm -rf CMSSW_7_1_47
