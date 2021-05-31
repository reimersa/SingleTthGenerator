# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: Configuration/GenProduction/python/B2G-RunIIWinter15wmLHE-00223-fragment.py --python_filename B2G-RunIIWinter15wmLHE-00223_1_cfg.py --eventcontent LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier LHE --fileout file:B2G-RunIIWinter15wmLHE-00223.root --conditions MCRUN2_71_V1::All --step LHE --no_exec --mc -n 100
import FWCore.ParameterSet.Config as cms
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
from FWCore.ParameterSet.VarParsing import VarParsing
import os

# gridpack    = '/afs/cern.ch/user/a/areimers/SingleTth/Generator/gridpacks/SingleTth_VariableMassH/SingleTth_VariableMassH_MT700_MH450_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
# outfilename = 'gsiftp://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/store/user/areimers/test_lhe.root'
# nevents     = 20
gridpack    = ''
outfilename = ''
nevents     = -1
nThreads    = -1


# USER OPTIONS
options = VarParsing('analysis')
options.register('gridpack',    gridpack,    mytype=VarParsing.varType.string)
options.register('outfilename', outfilename, mytype=VarParsing.varType.string)
options.register('nevents',     nevents,     mytype=VarParsing.varType.int)
options.register('nThreads',    nThreads,    mytype=VarParsing.varType.int)
options.parseArguments()
gridpack    = os.path.abspath(options.gridpack)
nevents     = options.nevents
nThreads    = options.nThreads
outfilename = 'file:' + os.path.abspath(options.outfilename)


if gridpack is '' or outfilename is '' or nevents is -1:
    raise ValueError('At least one of the 4 mandatory options is not set, please give all 4 options.')


print "--> gridpack    = '%s'" % gridpack
print "--> nevents     = %s"   % nevents
print "--> nThreads    = %s"   % nThreads
print "--> outfilename = '%s'" % outfilename






process = cms.Process('LHE')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(nevents)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('Configuration/GenProduction/python/B2G-RunIIWinter15wmLHE-00223-fragment.py nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.LHEoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.LHEEventContent.outputCommands,
    fileName = cms.untracked.string(outfilename),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('LHE')
    )
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(nevents),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring(gridpack)
)


# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.LHEoutput_step = cms.EndPath(process.LHEoutput)

# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.endjob_step,process.LHEoutput_step)

# #Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(nThreads)
process.options.numberOfStreams=cms.untracked.uint32(0)

# customisation of the process.

# Customisation from command line
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate() # set random number each cmsRun


# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
