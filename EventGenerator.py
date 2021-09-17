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
from collections import OrderedDict

import ROOT
from ROOT import gROOT, gStyle, gPad, TLegend, TFile, TCanvas, Double, TF1, TH2D, TGraph, TGraph2D, TGraphAsymmErrors, TLine,\
                 kBlack, kRed, kBlue, kAzure, kCyan, kGreen, kGreen, kYellow, kOrange, kMagenta, kViolet,\
                 kSolid, kDashed, kDotted
from math import sqrt, log, floor, ceil
from array import array

# from preferred_configurations import *
from tdrstyle_all import *
import tdrstyle_all as TDR


class EventGenerator:
    def __init__(self, processname, year, tag, configs, singularityfolder, workdir, workarea, scriptfolder, cardfolder, mgfolder, generatorfolder, gridpackfolder, arch_tag_gp, arch_tag, cmssw_tag_gp, cmssw_path_gp, T2_director, T2_path, T2_director_root, campaign, folderstructure, maxindex=100, nevents=1000, submit=False):
        self.processname = processname
        self.year = year
        self.tag = tag
        self.configs = configs
        self.singularityfolder = singularityfolder
        self.workdir = workdir
        self.workarea = workarea
        self.scriptfolder = scriptfolder
        self.cardfolder = cardfolder
        self.mgfolder = mgfolder
        self.generatorfolder = generatorfolder
        self.gridpackfolder = gridpackfolder
        self.arch_tag = arch_tag
        self.arch_tag_gp = arch_tag_gp
        self.cmssw_tag_gp = cmssw_tag_gp
        self.cmssw_path_gp = cmssw_path_gp
        self.T2_director = T2_director
        self.T2_path = T2_path
        self.T2_director_root = T2_director_root
        self.campaign = campaign
        self.folderstructure = folderstructure
        self.maxindex = maxindex
        self.nevents = nevents
        self.submit = submit


    def ProduceCards(self, pdfs_per_year):

        idx = 0
        for config in self.configs:
            mt, mh = get_mt_mh(config=config)
            if self.submit:
                ensureDirectory(self.cardfolder+'/%s/%s' % (self.processname, self.year))
                make_card(card_template_folder=self.cardfolder, card_output_folder=self.cardfolder+'/%s/%s' % (self.processname, self.year), processname=self.processname, tag=self.tag, mt=mt, mh=mh, lhapdfid=pdfs_per_year[self.year])
                print green('--> Produced cards for sample no. %i.' % (idx+1))
            idx += 1

        if not self.submit:
            print yellow('--> Would have produced cards for %i samples.' % (idx))



    def SubmitGridpacks(self):
        # Submit gridpacks based on cards created above
        ensureDirectory(os.path.join(self.gridpackfolder, self.processname, str(self.year)))
        for config in self.configs:
            mt, mh = get_mt_mh(config=config)
            jobname = samplename = get_samplename(basename=self.processname, mt=mt, mh=mh, tag=self.tag)
            submissionsettings = OrderedDict([
                ('executable' ,  os.path.join(self.scriptfolder, 'singularity_wrapper.sh')),
                ('output'     ,  os.path.join(self.workdir, 'gridpacks_$(ClusterId)_$(ProcId).out')),
                ('error'      ,  os.path.join(self.workdir, 'gridpacks_$(ClusterId)_$(ProcId).err')),
                ('log'        ,  os.path.join(self.workdir, 'gridpacks_$(ClusterId).log')),
                ('environment', 'ClusterId=$(ClusterId);ProcId=$(ProcId);SCRAM_ARCH=%s;CMSSW_VERSION=%s;PATH=%s;LD_LIBRARY_PATH=%s;KRB5CCNAME=$KRB5CCNAME' % (self.arch_tag_gp, self.cmssw_tag_gp, os.environ['PATH'], os.environ['LD_LIBRARY_PATH'])),
                ('arguments'  ,   '"%s %s %s %s %s %s %s"' % (os.path.join(self.scriptfolder, 'run_gridpacks.sh'), self.mgfolder, jobname, self.cardfolder+'/%s/%s' % (self.processname, str(self.year)), os.path.join(self.gridpackfolder, self.processname, str(self.year)), 'local', self.cmssw_path_gp)),
                ('transfer_output_files', '""'),
                ('stream_output', 'True'),
                ('stream_error', 'True'),
                ('+JobFlavour', '"longlunch"'), # workday
                ('queue'      , '')
            ])
            submissionscriptname = os.path.join(self.scriptfolder, 'submit_gridpack.sub')
            create_submitfile(settings=submissionsettings, outfilename=submissionscriptname)
            command = 'condor_submit %s' % (submissionscriptname)
            if self.submit:
                os.system(command)
            else:
                print command

        if self.submit: print green('--> Done submitting gridpacks.')
        else:      print yellow('--> Would have submitted gridpacks.')



    def SubmitGenerationStep(self, generation_step, ncores=8, runtime=(10,00), mode='new'):
        # Submit event generation jobs to the SLURM cluster

        if mode is not 'new' and mode is not 'resubmit':
            raise ValueError('Value \'%s\' is invalid for variable \'mode\'.' % mode)

        nminutes = runtime[0]*60. + runtime[1]
        queue = ''
        if nminutes <= 20: queue = 'espresso'
        elif nminutes <= 60: queue  = 'microcentury'
        elif nminutes <= 2*60: queue  = 'longlunch'
        elif nminutes <= 8*60: queue  = 'workday'
        elif nminutes <= 24*60: queue  = 'tomorrow'
        elif nminutes <= 3*24*60: queue  = 'testmatch'
        elif nminutes <= 7*24*60: queue  = 'nextweek'
        else: raise ValueError('Runtime exceeds 7 days, please choose something a bit faster.')

        commandfilebase = ''
        if mode is 'new':        commandfilebase = self.generatorfolder + '/commands/%s_' % (self.folderstructure[generation_step]['jobnametag'])
        elif mode is 'resubmit': commandfilebase = self.generatorfolder + '/commands/resubmit_%s_' % (self.folderstructure[generation_step]['jobnametag'])

        # Create command file for array of jobs
        for config in self.configs:
            mt, mh = get_mt_mh(config=config)
            jobname = samplename = get_samplename(basename=self.processname, mt=mt, mh=mh, tag=self.tag)
            commandfilename = commandfilebase + jobname + '.txt'
            f = open(commandfilename, 'w')
            indices = -1
            if mode is 'new':
                indices = range(self.maxindex)
            elif mode is 'resubmit':
                print green('--> Now checking for missing files on T2 for generation step \'%s\' of job \'%s\'...' % (generation_step, jobname))
                indices = missing_indices = findMissingFilesT2(filepath=self.T2_director+self.T2_path+'/'+self.folderstructure[generation_step]['pathtag']+'/'+jobname, filename_base=self.folderstructure[generation_step]['outfilenamebase'], maxindex=self.maxindex, generatorfolder=self.generatorfolder, generation_step=generation_step)
            njobs = 0
            for i in indices:
                outfilename = '%s_%i.root' % (self.folderstructure[generation_step]['outfilenamebase'], i+1)
                command = ''
                if generation_step is not 'GENSIM':
                    infilename   = self.T2_director_root+self.T2_path+'/'+self.folderstructure[generation_step]['infilepathtag']+'/'+jobname+'/%s_%i.root' % (self.folderstructure[generation_step]['infilenamebase'], i+1)
                    command = getcmsRunCommand(pset=self.folderstructure[generation_step]['pset'], infilename=infilename, outfilename=outfilename, N=self.nevents, ncores=ncores)
                else:
                    infilename   = self.gridpackfolder + '/' + jobname + '_' + self.arch_tag_gp + '_' + self.cmssw_tag_gp + '_tarball.tar.xz'
                    command = getcmsRunCommand(pset=self.folderstructure[generation_step]['pset'], gridpack=infilename, outfilename=outfilename, N=self.nevents, ncores=ncores)
                f.write(command + '\n')
                njobs += 1
            f.close()
            clusterjobname = ''
            if mode is 'new':        clusterjobname = '%s' % (self.folderstructure[generation_step]['jobnametag'])
            elif mode is 'resubmit': clusterjobname = 'resubmit_%s' % (self.folderstructure[generation_step]['jobnametag'])

            submissionsettings = OrderedDict([
                ('executable' ,  os.path.join(self.scriptfolder, 'singularity_wrapper_cmsrun.sh')),
                ('output'     ,  os.path.join(self.workdir, '%s_$(ClusterId)_$(ProcId).out' % (self.folderstructure[generation_step]['jobnametag']))),
                ('error'      ,  os.path.join(self.workdir, '%s_$(ClusterId)_$(ProcId).err' % (self.folderstructure[generation_step]['jobnametag']))),
                ('log'        ,  os.path.join(self.workdir, '%s_$(ClusterId).log' % (self.folderstructure[generation_step]['jobnametag']))),
                ('environment', 'ClusterId=$(ClusterId);ProcId=$(ProcId);X509_VOMS_DIR=/cvmfs/grid.cern.ch/etc/grid-security/vomsdir;X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates;X509_USER_PROXY=%s;SCRAM_ARCH=%s;CMSSW_VERSION=%s;PATH=%s;LD_LIBRARY_PATH=%s;KRB5CCNAME=$KRB5CCNAME' % (os.environ['X509_USER_PROXY'], self.arch_tag_gp, self.folderstructure[generation_step]['cmsswtag'], os.environ['PATH'], os.environ['LD_LIBRARY_PATH'])),
                ('arguments'  ,   '"%s %s %s %s %s %s %s"' % (os.path.join(self.scriptfolder, 'submit_cmsRun_command.sh'), self.generatorfolder, self.arch_tag_gp, self.workarea+'/'+self.folderstructure[generation_step]['cmsswtag'], self.T2_director+self.T2_path+'/'+self.folderstructure[generation_step]['pathtag']+'/'+jobname, commandfilename, os.path.join(self.scriptfolder, 'copy_files_gfal.sh'))),
                # ('stream_output', 'True'),
                ('stream_error', 'True'),
                ('transfer_output_files', '""'),
                ('RequestCpus', ncores),
                ('+MaxRuntime', 60.*nminutes),
                ('+JobFlavour', '"%s"' % queue),
                # ('+JobFlavour', '"espresso"'),
                ('queue'      , njobs)
                # ('queue'      , "")
            ])
            submissionscriptname = os.path.join(self.scriptfolder, 'submit_cmsrun_%s.sub' % (self.folderstructure[generation_step]['jobnametag']))
            create_submitfile(settings=submissionsettings, outfilename=submissionscriptname)

            command = 'condor_submit %s' % (submissionscriptname)
            if njobs > 0:
                if self.submit:
                    # print command
                    os.system(command)
                    print green('  --> Submitted an array of %i jobs for for generation step \'%s\' of job \'%s\''%(njobs, generation_step, jobname))
                else:
                    print command
                    print yellow('  --> Would submit an array of %i jobs'%(njobs))
            else:
                if mode is 'resubmit':
                    print green('  --> No jobs to resubmit.')
                else:
                    print green('  --> No jobs to submit.')





    def RemoveSamples(self, generation_step):
        # Remove old samples from the T2 if they are no longer needed. This saves A LOT of space. This can run locally from the login node since it recursively deletes the entire folder.
        # Loop through samples to find all that should be deleted
        commands = []
        for processname in self.processnames:
            allowed_configs = []
            for config in self.configs:
                if not is_config_excluded_for_process(config=config, processname=processname, preferred_configurations=self.preferred_configurations):
                    allowed_configs.append(config)
                else:
                    print yellow('--> Skip config %s for process \'%s\'' % (config, processname))
            for config in allowed_configs:
                for lamb in self.lambdas:
                    mlq, mps, mch = get_mlq_mps_mch(preferred_configurations=self.preferred_configurations, config=config)
                    jobname       = get_jobname(processname=processname, mlq=mlq, mps=mps, mch=mch, lamb=lamb, tag=self.tag)
                    samplepath    = self.T2_director+self.T2_path+'/'+self.folderstructure[generation_step]['pathtag']+'/'+jobname
                    command       = 'LD_LIBRARY_PATH=\'\' PYTHONPATH=\'\' gfal-rm -r %s' % (samplepath)
                    # print command
                    if self.submit:
                        print green('--> Will delete files from job %s for generation step %s'%(jobname, generation_step))
                    else:
                        print yellow('--> Would delete files from job %s for generation step %s'%(jobname, generation_step))
                    commands.append(command)
        if self.submit:
            execute_commands_parallel(commands=commands, niceness=None)
