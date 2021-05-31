import os, sys, math
import glob
from os.path import isfile, join
import subprocess
import time
import parse
from operator import itemgetter
import importlib
# from utils import *

workdir = '/eos/user/a/areimers/workdir'

print len(glob.glob('%s/*' % workdir))
for file in glob.glob('%s/*' % workdir):
    # print file
    os.remove(file)
