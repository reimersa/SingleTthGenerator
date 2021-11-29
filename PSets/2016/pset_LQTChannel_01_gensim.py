# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-05559-fragment.py --python_filename B2G-RunIISummer15wmLHEGS-05559_1_cfg.py --eventcontent RAWSIM,LHE --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:B2G-RunIISummer15wmLHEGS-05559.root --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed=int() --step LHE,GEN,SIM --magField 38T_PostLS1 --no_exec --mc -n 100
import FWCore.ParameterSet.Config as cms
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
from FWCore.ParameterSet.VarParsing import VarParsing
from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
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

process = cms.Process('SIM')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
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
    annotation = cms.untracked.string('Configuration/GenProduction/python/B2G-RunIISummer15wmLHEGS-05559-fragment.py nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string(outfilename),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# process.LHEoutput = cms.OutputModule("PoolOutputModule",
#     splitLevel = cms.untracked.int32(0),
#     eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
#     outputCommands = process.LHEEventContent.outputCommands,
#     fileName = cms.untracked.string('file:B2G-RunIISummer15wmLHEGS-05559_inLHE.root'),
#     dataset = cms.untracked.PSet(
#         filterName = cms.untracked.string(''),
#         dataTier = cms.untracked.string('LHE')
#     )
# )

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    maxEventsToPrint = cms.untracked.int32(1),
    ExternalDecays = cms.PSet(Tauola = cms.untracked.PSet(TauolaPolar, TauolaDefaultInputCards ), parameterSets = cms.vstring('Tauola')),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PSweightsSettings = cms.vstring('UncertaintyBands:doVariations = on',
            'UncertaintyBands:List = {isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,isrDefHi isr:muRfac=0.5,fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,isrConHi isr:muRfac=0.25,fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0,fsr_G2GG_muR_dn fsr:G2GG:muRfac=0.5,fsr_G2GG_muR_up fsr:G2GG:muRfac=2.0,fsr_G2QQ_muR_dn fsr:G2QQ:muRfac=0.5,fsr_G2QQ_muR_up fsr:G2QQ:muRfac=2.0,fsr_Q2QG_muR_dn fsr:Q2QG:muRfac=0.5,fsr_Q2QG_muR_up fsr:Q2QG:muRfac=2.0,fsr_X2XG_muR_dn fsr:X2XG:muRfac=0.5,fsr_X2XG_muR_up fsr:X2XG:muRfac=2.0,fsr_G2GG_cNS_dn fsr:G2GG:cNS=-2.0,fsr_G2GG_cNS_up fsr:G2GG:cNS=2.0,fsr_G2QQ_cNS_dn fsr:G2QQ:cNS=-2.0,fsr_G2QQ_cNS_up fsr:G2QQ:cNS=2.0,fsr_Q2QG_cNS_dn fsr:Q2QG:cNS=-2.0,fsr_Q2QG_cNS_up fsr:Q2QG:cNS=2.0,fsr_X2XG_cNS_dn fsr:X2XG:cNS=-2.0,fsr_X2XG_cNS_up fsr:X2XG:cNS=2.0,isr_G2GG_muR_dn isr:G2GG:muRfac=0.5,isr_G2GG_muR_up isr:G2GG:muRfac=2.0,isr_G2QQ_muR_dn isr:G2QQ:muRfac=0.5,isr_G2QQ_muR_up isr:G2QQ:muRfac=2.0,isr_Q2QG_muR_dn isr:Q2QG:muRfac=0.5,isr_Q2QG_muR_up isr:Q2QG:muRfac=2.0,isr_X2XG_muR_dn isr:X2XG:muRfac=0.5,isr_X2XG_muR_up isr:X2XG:muRfac=2.0,isr_G2GG_cNS_dn isr:G2GG:cNS=-2.0,isr_G2GG_cNS_up isr:G2GG:cNS=2.0,isr_G2QQ_cNS_dn isr:G2QQ:cNS=-2.0,isr_G2QQ_cNS_up isr:G2QQ:cNS=2.0,isr_Q2QG_cNS_dn isr:Q2QG:cNS=-2.0,isr_Q2QG_cNS_up isr:Q2QG:cNS=2.0,isr_X2XG_cNS_dn isr:X2XG:cNS=-2.0,isr_X2XG_cNS_up isr:X2XG:cNS=2.0}',
            'UncertaintyBands:nFlavQ = 4',
            'UncertaintyBands:MPIshowers = on',
            'UncertaintyBands:overSampleFSR = 10.0',
            'UncertaintyBands:overSampleISR = 10.0',
            'UncertaintyBands:FSRpTmin2Fac = 20',
            'UncertaintyBands:ISRpTmin2Fac = 1'),
        parameterSets = cms.vstring('pythia8CommonSettings', 'pythia8CUEP8M1Settings', 'pythia8PSweightsSettings')
    )
)


process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    nEvents = cms.untracked.uint32(nevents),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring(gridpack)
)


# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)
# process.LHEoutput_step = cms.EndPath(process.LHEoutput)

# Schedule definition
# process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step,process.LHEoutput_step)
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.simulation_step,process.endjob_step,process.RAWSIMoutput_step)

# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions
process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(nevents)

# Customisation from command line

randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate() # set random number each cmsRun
