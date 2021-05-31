#!/bin/bash

export SCRAM_ARCH=slc6_amd64_gcc481

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_7_1_15_patch1/src ] ; then
  echo release CMSSW_7_1_15_patch1 already exists
else
  scram p CMSSW CMSSW_7_1_15_patch1
fi
cd CMSSW_7_1_15_patch1/src
eval `scram runtime -sh`

# Download fragment from McM
curl -s -k https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/B2G-RunIIWinter15wmLHE-00223 --retry 3 --create-dirs -o Configuration/GenProduction/python/B2G-RunIIWinter15wmLHE-00223-fragment.py
scram b
cd ../..

# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/B2G-RunIIWinter15wmLHE-00223-fragment.py --python_filename B2G-RunIIWinter15wmLHE-00223_1_cfg.py --eventcontent LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier LHE --fileout file:B2G-RunIIWinter15wmLHE-00223.root --conditions MCRUN2_71_V1::All --step LHE --no_exec --mc -n 100

rm -rf CMSSW_7_1_15_patch1
