#! /usr/bin/env python

import os, sys, math
from os.path import isfile, join
import subprocess
import time
import parse
from operator import itemgetter
import importlib
from utils import *
from functions import *

import ROOT
from ROOT import gROOT, gStyle, gPad, TLegend, TFile, TCanvas, Double, TF1, TH2D, TGraph, TGraph2D, TGraphAsymmErrors, TLine,\
                 kBlack, kRed, kBlue, kAzure, kCyan, kGreen, kGreen, kYellow, kOrange, kMagenta, kViolet,\
                 kSolid, kDashed, kDotted
from math import sqrt, log, floor, ceil
from array import array

from tdrstyle_all import *
import tdrstyle_all as TDR

from EventGenerator import *





processname = 'SingleTth_VariableMassH'
# mhs = [75, 125, 175, 250, 350, 450]
# mts = [700]
mhs = [75, 175, 450]
mts = [600, 800, 900, 1000, 1100, 1200]

mass_configurations = []
for mt in mts:
    for mh in mhs:
        # if (mt == 1100 and mh == 450) or (mt == 1200 and mh == 25): continue
        mass_configurations.append({'mt': mt, 'mh': mh})


# mass_configurations = [{'mt': 1100, 'mh': 450}, {'mt': 1200, 'mh': 75}]



# mt_cross = 700
# mh_cross = 300

# PDF CMS standard (Paolo):
# 2016 LO:       263000
# 2016 NLO:      260000
# 2017 CP5:      303600
# 2018 CP5:      303600 (same as 2017)
# 2017/18 CP2:   315200 for 2017/8
pdfs_per_year = {
    2016: 263000,
    2017: 303600,
    2018: 303600
}


# cmsswdir = '/work/areimers/CMSSW_10_6_12'
# lhefolder = '/work/areimers/SingleTth/LHEevents'





tag              = ''    # tags are auto-formatted to '_XXXX'
maxindex         = 1000  # Number of samples per configuration
nevents          = 100   # Events per sample


username         = os.environ['USER']
eosfolder        = os.environ['EOSHOME']
arch_tag_gp      = 'slc6_amd64_gcc630'
arch_tag         = os.environ['SCRAM_ARCH']
cmssw_tag_gp     = 'CMSSW_9_3_16'
year             = 2017
campaign         = str(year)

home             = os.environ['HOME']
cmssw_path_gp    = os.path.join(home, cmssw_tag_gp, 'src')
generatorfolder  = os.environ['GENERATORPATH']
workarea         = home
workdir          = os.path.abspath(os.path.join(home, 'workdir_eos'))
# mgfolder         = os.path.abspath(os.path.join(home, 'genproductions', 'bin', 'MadGraph5_aMCatNLO'))
mgfolder         = os.path.abspath(os.path.join(home, 'genproductions_27x', 'bin', 'MadGraph5_aMCatNLO'))
mgfolder_local   = os.environ['MGDIR']
singularityfolder= os.environ['SINGULARITY_IMAGE']
scriptfolder     = os.path.abspath(os.path.join(generatorfolder, 'scripts'))
gridpackfolder   = os.path.abspath(os.path.join(eosfolder, 'gridpacks/%s' % (processname)))
cardfolder       = os.path.abspath(os.path.join(generatorfolder, 'cards'))
psetfolder       = os.path.abspath(os.path.join(os.path.join(generatorfolder, 'PSets', campaign)))
T2_director      = 'gsiftp://storage01.lcg.cscs.ch/'
T2_director_root = 'root://storage01.lcg.cscs.ch/'
T2_path          = '/pnfs/lcg.cscs.ch/cms/trivcat/store/user/'+ username



folderstructure = {
    'GENSIM': {
        'pset':            psetfolder+'/pset_new_01_gensim.py',
        'cmsswtag':        'CMSSW_9_3_6',
        'jobnametag':      'gensim',
        'outfilenamebase': 'GENSIM',
        'pathtag':         'GENSIM/SingleTth'
    },
    'DR': {
        'pset':            psetfolder+'/pset_new_02_dr.py',
        'cmsswtag':        'CMSSW_9_4_7',
        'jobnametag':      'dr',
        'outfilenamebase': 'DR',
        'infilepathtag':   'GENSIM/SingleTth',
        'infilenamebase':  'GENSIM',
        'pathtag':         'DR/SingleTth'
    },
    'AOD': {
        'pset':            psetfolder+'/pset_new_03_aod.py',
        'cmsswtag':        'CMSSW_9_4_7',
        'jobnametag':      'aod',
        'outfilenamebase': 'AOD',
        'infilepathtag':   'DR/SingleTth',
        'infilenamebase':  'DR',
        'pathtag':         'AOD/SingleTth'
    },
    'MINIAOD': {
        'pset':            psetfolder+'/pset_new_04_miniaod.py',
        'cmsswtag':        'CMSSW_9_4_7',
        'jobnametag':      'miniaod',
        'outfilenamebase': 'MINIAOD',
        'infilepathtag':   'AOD/SingleTth',
        'infilenamebase':  'AOD',
        'pathtag':         'MINIAOD/SingleTth'
    }

}

ensureDirectory(workdir)




# SINGULARITYENV_ClusterId=0 SINGULARITYENV_ProcId=1 SINGULARITYENV_X509_VOMS_DIR=/cvmfs/grid.cern.ch/etc/grid-security/vomsdir SINGULARITYENV_X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates SINGULARITYENV_X509_USER_PROXY=/afs/cern.ch/user/a/areimers/.voms_proxy SINGULARITYENV_CMSSW_VERSION=CMSSW_8_0_21 SINGULARITYENV_WORKDIR=/afs/cern.ch/user/a/areimers/SingleTth/Generator/scripts SINGULARITYENV_LD_LIBRARY_PATH=/afs/cern.ch/user/a/areimers/SingleTth/Generator/PSets/2017/CMSSW_8_0_21/biglib/slc6_amd64_gcc530:/afs/cern.ch/user/a/areimers/SingleTth/Generator/PSets/2017/CMSSW_8_0_21/lib/slc6_amd64_gcc530:/afs/cern.ch/user/a/areimers/SingleTth/Generator/PSets/2017/CMSSW_8_0_21/external/slc6_amd64_gcc530/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_21/biglib/slc6_amd64_gcc530:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_21/lib/slc6_amd64_gcc530:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_21/external/slc6_amd64_gcc530/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/llvm/3.8.0-giojec2/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0/lib:/eos/home-a/areimers/MG5_aMC_v2_8_3_2/HEPTools/hepmc/lib SINGULARITYENV_PREPEND_PATH=/cvmfs/cms.cern.ch/share/overrides/bin:/afs/cern.ch/user/a/areimers/SingleTth/Generator/PSets/2017/CMSSW_8_0_21/bin/slc6_amd64_gcc530:/afs/cern.ch/user/a/areimers/SingleTth/Generator/PSets/2017/CMSSW_8_0_21/external/slc6_amd64_gcc530/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_21/bin/slc6_amd64_gcc530:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_21/external/slc6_amd64_gcc530/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/llvm/3.8.0-giojec2/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0/bin:/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/usr/sue/bin:/usr/lib64/qt-3.3/bin:/usr/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin singularity shell --bind /tmp:/tmp --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs /eos/home-a/areimers/slc6_latest.sif





submit = True


EventGenerator = EventGenerator(processname=processname, year=year, tag=tag, configs=mass_configurations, singularityfolder=singularityfolder, workdir=workdir, workarea=workarea, scriptfolder=scriptfolder, cardfolder=cardfolder, mgfolder=mgfolder, generatorfolder=generatorfolder, gridpackfolder=gridpackfolder, arch_tag_gp=arch_tag_gp, arch_tag=arch_tag, cmssw_tag_gp=cmssw_tag_gp, cmssw_path_gp=cmssw_path_gp, T2_director=T2_director, T2_path=T2_path, T2_director_root=T2_director_root, campaign=campaign, folderstructure=folderstructure, maxindex=maxindex, nevents=nevents, submit=submit)
# EventGenerator.ProduceCards(pdfs_per_year=pdfs_per_year)
# EventGenerator.SubmitGridpacks()
# EventGenerator.SubmitGenerationStep(generation_step='GENSIM', ncores=1, runtime=(3,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='GENSIM', ncores=1, runtime=(3,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='DR', ncores=1, runtime=(2,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='DR', ncores=1, runtime=(2,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='AOD', ncores=1, runtime=(2,00), mode='new')
# EventGenerator.SubmitGenerationStep(generation_step='AOD', ncores=1, runtime=(2,00), mode='resubmit')
# EventGenerator.SubmitGenerationStep(generation_step='MINIAOD', ncores=1, runtime=(2,00), mode='new')
EventGenerator.SubmitGenerationStep(generation_step='MINIAOD', ncores=1, runtime=(2,00), mode='resubmit')





#
