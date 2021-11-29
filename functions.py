# Author: Arne Reimers
import os, sys
from os.path import isfile, join
from fnmatch import fnmatch
import subprocess
import time
import math
from math import sqrt, log, floor, ceil
from bisect import bisect_left
from utils import *
from tqdm import tqdm

def get_samplename(basename, mt, mh, tag):
    return '%s_MT%i_MH%i%s' % (basename, mt, mh, format_tag(tag))

def get_mt_mh(config):
    return (config['mt'], config['mh'])

def create_submitfile(settings, outfilename):
    # 'settings' must be a dictionary, with keys corresponding to the names of the .sub settings and the values corresponding to their values as a single string.

    with open(outfilename, 'wr') as f:
        newlines = []
        for setting in settings:
            line = '%s = %s\n' % (setting, settings[setting])
            if setting == 'queue':
                line = line.replace(' = ', ' ')
            newlines.append(line)
        for l in newlines:
            f.write(l)





def make_card_singletth(card_template_folder, card_output_folder, processname, tag, mt, mh, lhapdfid, verbose=True):

    # PDF CMS standard (Paolo):
    # 2016 LO:       263000
    # 2016 NLO:      260000
    # 2017 CP5:      303600
    # 2018 CP5:      303600 (same as 2017)
    # 2017/18 CP2:   315200 for 2017/8
    samplename = get_samplename(basename=processname, mt=mt, mh=mh, tag=tag)
    cardbasename = processname + '_template'
    cardtypes = ['proc_card.dat', 'run_card.dat', 'customizecards.dat', 'extramodels.dat']
    cards = [card_template_folder + '/' + cardbasename + '_' + c for c in cardtypes]

    newcards = []
    for card in cards:
        template = card
        newcard = card.replace('%s_template' % (processname), samplename).replace(card_template_folder, card_output_folder)
        newcards.append(newcard)

        # create newcard
        command = 'cp %s %s' % (template, newcard)
        os.system(command)

    outputfoldername = samplename

    replacement_dict = {
        'MH':      mh,
        'MT':      mt,
        'SCALE':   mt,
        'OUTPUT':  outputfoldername,
        'PDF':     lhapdfid
    }

    # replace values in the cards
    for card in newcards:
        replace_placeholders(card=card, replacement_dict=replacement_dict, verbose=verbose)
    if verbose:
        print green('--> Done making one set of cards.\n')


def make_card_lqtchannel(card_template_folder, card_output_folder, processname, tag, mlq, lhapdfid, verbose=True):

    samplename = '%s_M%i%s' % (processname, mlq, format_tag(tag))
    cardbasename = processname + '_template'
    cardtypes = ['proc_card.dat', 'run_card.dat', 'customizecards.dat', 'extramodels.dat']
    cards = [card_template_folder + '/' + cardbasename + '_' + c for c in cardtypes]

    newcards = []
    for card in cards:
        template = card
        newcard = card.replace('%s_template' % (processname), samplename).replace(card_template_folder, card_output_folder)
        newcards.append(newcard)

        # create newcard
        command = 'cp %s %s' % (template, newcard)
        os.system(command)

    outputfoldername = samplename

    replacement_dict = {
        'MLQ':     mlq,
        'OUTPUT':  outputfoldername,
        'PDF':     lhapdfid
    }

    # replace values in the cards
    for card in newcards:
        replace_placeholders(card=card, replacement_dict=replacement_dict, verbose=verbose)
    if verbose:
        print green('--> Done making one set of cards.\n')

def replace_placeholders(card, replacement_dict, identifier = '$', verbose=False):
    fin = open(card,'r')
    lines = fin.readlines()
    newlines = []
    lineidx = 0
    for line in lines:
        lineidx += 1
        newline = line
        for key in replacement_dict.keys():
            pattern = identifier + key
            if pattern in line:
                newline = line.replace(pattern, str(replacement_dict[key]))
                if verbose:
                    print green('In file \'%s\': replaced %s with %s in line %i' % (card, pattern, str(replacement_dict[key]), lineidx))
        if identifier in newline and not newline.strip()[0] == '#':
            print yellow('found identifier in newline, meaning it hasn\'t been replaced. Line is: %s' % (newline[:-1]))
        newlines.append(newline)

    fin.close()

    fout = open(card, 'w')
    for l in newlines:
        fout.write(l)
    fout.close()
    if verbose:
        print green('--> Successfully created card %s' % (card))



def get_filelist_crossbr(filepath, short, tag):
    postfix = ''

    if short:
        filenames = [f for f in os.listdir(filepath) if isfile(join(filepath, f)) and postfix in f and tag in f and '_short' in f]
    else:
        filenames = [f for f in os.listdir(filepath) if isfile(join(filepath, f)) and postfix in f and tag in f and not '_short' in f]
    return (filenames)

def check_shortfiles(filepath, tag):
    filenames = get_filelist_crossbr(filepath=filepath, short=True, tag=tag)

        # check if the shortfile contains necessary info, otherwise delete it
    for filename in filenames:
        is_param_card = True if 'param_card' in filename else False
        infilename = join(filepath, filename)
        fin = open(infilename, 'r')
        lines = fin.readlines()
        found_start = False
        keep_file = False
        if not is_param_card:
            found_systs = False
            for line in lines:
                if '  === Results Summary for run' in line or 'Summary:' in line: found_start = True
                if 'PDF variation' in line: found_systs = True
            keep_file = found_start and found_systs
        else:
            found_end = False
            for line in lines:
                if 'DECAY  9000005' in line: found_start = True
                if line[0] == '#' and not line[1] == ' ': found_end = True
            keep_file = found_start and found_end
        if not keep_file:
            print yellow('Removing incomplete file %s' % (infilename))
            os.remove(infilename)




def XsecTotErr(sigma,*errs,**kwargs):
    """Helpfunction to calculate total error."""
    absolute = kwargs.get('abs', False)
    err2 = 0
    for err in errs:
        err2 += err**2
    toterr = sqrt(err2)
    if not absolute:
        toterr *= sigma/100.
    return toterr

def get_all_combinations(preferred_configurations, mlq_stepsize=90, mch_exp_stepsize=0.03):
    all_combinations = {}
    mlq_min = min(preferred_configurations.keys())
    mlq_max = max(preferred_configurations.keys())
    mch_min = 999999999
    mch_max = 0
    for mlq in preferred_configurations.keys():
        for mch in preferred_configurations[mlq].keys():
            mch_min = min(mch_min, mch)
            mch_max = max(mch_max, mch)

    for mlq in range(mlq_min, mlq_max+mlq_stepsize, mlq_stepsize):
        all_combinations[mlq] = []
        for mch_exp in range(int(math.log(mch_min, 10)*100), int(math.log(mch_max, 10)*100) + int(mch_exp_stepsize*100), int(mch_exp_stepsize*100)):
            mch_exp = float(mch_exp / 100.)
            mch = int(round(10**(float(mch_exp))))
            all_combinations[mlq].append(mch)
    return all_combinations


def get_best_lambda(mlq):
    return float(1.1/2. * (mlq/1000.))

def findMissingFilesT2(filepath, filename_base, maxindex, generatorfolder, generation_step):
    missing_indices = []
    filename_base = filepath+'/'+filename_base
    min_size = 0
    if generation_step is 'GENSIM':
        min_size = 1E7
    elif generation_step is 'DR':
        min_size = 1E8
    pbar = tqdm(range(maxindex), desc="Files checked")
    for idx in pbar:
        filename = filename_base + '_' + str(idx+1) + '.root'
        # print 'didn\'t find file %s, going to try to open it' % (filename)
        result = subprocess.Popen(['/bin/bash', '%s/check_T2_file.sh' % (generatorfolder), filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()
        returncode = result.returncode
        if returncode > 0: # opening failed
            # print 'opening failed for index %i' % (idx+1)
            missing_indices.append(idx)
        else:
            size = int(output.split()[4])
            # print size
            if size < min_size: # file too small.
                print yellow('  --> size for index %i is %i, resubmit.' % (idx+1, size))
                missing_indices.append(idx)

    return missing_indices

def findMissingFilesT3(filepath, filename_base, maxindex, generation_step):
    missing_indices = []
    filename_base = filepath+'/'+filename_base
    min_size = 0
    if generation_step is 'Tuples_GENSIM':
        min_size = 1E5
    if generation_step is 'Tuples_NANOAOD':
        min_size = 1E5
    for idx in range(maxindex):
        filename = filename_base + '_' + str(idx+1) + '.root'
        result = subprocess.Popen(['ls', '-lrt', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()
        returncode = result.returncode
        if returncode > 0: # opening failed
            print 'opening failed for index %i' % (idx+1)
            missing_indices.append(idx)
        else:
            size = int(output.split()[4])
            if size < min_size: # file too small.
                print yellow('  --> size for index %i is %i, resubmit.' % (idx+1, size))
                missing_indices.append(idx)
    return missing_indices

def getcmsRunCommand(pset, outfilename, N, ncores, infilename=None, gridpack=None):
    """Submit PSet config file and gridpack to SLURM batch system."""

    if gridpack is not None and infilename is None:
        command = 'cmsRun %s gridpack=%s outfilename=%s nevents=%i nThreads=%i' % (pset, gridpack, outfilename, N, ncores)
    elif infilename is not None and gridpack is None:
        command = 'cmsRun %s infilename=%s outfilename=%s nevents=%i nThreads=%i' % (pset, infilename, outfilename, N, ncores)
    return command
