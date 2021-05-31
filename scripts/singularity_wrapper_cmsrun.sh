#! /bin/bash

# first argument must be the executable, the remaining arguments are those passed to the executable

export WORKDIR=$PWD
export TARGETFOLDERNAME=$5

#for cmsRun
CMD="SINGULARITYENV_ClusterId=$ClusterId SINGULARITYENV_ProcId=$ProcId SINGULARITYENV_X509_VOMS_DIR=$X509_VOMS_DIR SINGULARITYENV_X509_CERT_DIR=$X509_CERT_DIR SINGULARITYENV_X509_USER_PROXY=$X509_USER_PROXY SINGULARITYENV_CMSSW_VERSION=$CMSSW_VERSION SINGULARITYENV_WORKDIR=$WORKDIR SINGULARITYENV_SCRAM_ARCH=$SCRAM_ARCH SINGULARITYENV_LD_LIBRARY_PATH=$LD_LIBRARY_PATH SINGULARITYENV_PREPEND_PATH=$PATH SINGULARITYENV_KRB5CCNAME=$KRB5CCNAME  singularity exec --cleanenv --contain --bind /tmp:/tmp --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs --bind /pool:/pool /eos/home-a/areimers/slc6_latest.sif $1 $2 $3 $4 $6"
echo $CMD
eval $CMD

cd $WORKDIR




#for gfal-XXX
CMD2="SINGULARITYENV_ClusterId=$ClusterId SINGULARITYENV_ProcId=$ProcId SINGULARITYENV_X509_VOMS_DIR=$X509_VOMS_DIR SINGULARITYENV_X509_CERT_DIR=$X509_CERT_DIR SINGULARITYENV_X509_USER_PROXY=$X509_USER_PROXY SINGULARITYENV_CMSSW_VERSION=$CMSSW_VERSION SINGULARITYENV_WORKDIR=$WORKDIR SINGULARITYENV_SCRAM_ARCH=$SCRAM_ARCH SINGULARITYENV_LD_LIBRARY_PATH=$LD_LIBRARY_PATH SINGULARITYENV_PREPEND_PATH=$PATH SINGULARITYENV_KRB5CCNAME=$KRB5CCNAME singularity exec --bind /tmp:/tmp --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs --bind /pool:/pool --bind /usr:/usr --bind /lib64:/lib64 --bind /etc:/etc --bind /bin:/bin /eos/home-a/areimers/slc6_latest.sif $7 $TARGETFOLDERNAME"
echo $CMD2
eval $CMD2



# success: SINGULARITYENV_ClusterId=2939035 SINGULARITYENV_ProcId=164 SINGULARITYENV_X509_VOMS_DIR=/cvmfs/grid.cern.ch/etc/grid-security/vomsdir SINGULARITYENV_X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates SINGULARITYENV_X509_USER_PROXY=/afs/cern.ch/user/a/areimers/.voms_proxy SINGULARITYENV_CMSSW_VERSION=CMSSW_9_3_6 SINGULARITYENV_WORKDIR=$WORKDIR SINGULARITYENV_SCRAM_ARCH=slc6_amd64_gcc630 SINGULARITYENV_LD_LIBRARY_PATH=/afs/cern.ch/user/a/areimers/CMSSW_10_2_22/biglib/slc6_amd64_gcc700:/afs/cern.ch/user/a/areimers/CMSSW_10_2_22/lib/slc6_amd64_gcc700:/afs/cern.ch/user/a/areimers/CMSSW_10_2_22/external/slc6_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/biglib/slc6_amd64_gcc700:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/lib/slc6_amd64_gcc700:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/external/slc6_amd64_gcc700/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/llvm/6.0.0-ogkkac/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib64:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/cuda/9.2.148/drivers::/eos/home-a/areimers/MG5_aMC_v2_8_3_2/HEPTools/hepmc/lib SINGULARITYENV_PREPEND_PATH=/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/bin:/usr/condabin:/cvmfs/cms.cern.ch/share/overrides/bin:/afs/cern.ch/user/a/areimers/CMSSW_10_2_22/bin/slc6_amd64_gcc700:/afs/cern.ch/user/a/areimers/CMSSW_10_2_22/external/slc6_amd64_gcc700/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/bin/slc6_amd64_gcc700:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/external/slc6_amd64_gcc700/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/llvm/6.0.0-ogkkac/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/gcc/7.0.0-omkpbe2/bin:/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/afs/cern.ch/cms/caf/scripts:/cvmfs/cms.cern.ch/common:/usr/sue/bin:/usr/lib64/qt-3.3/bin:/usr/condabin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin SINGULARITYENV_KRB5CCNAME=$KRB5CCNAME  singularity shell  --cleanenv --contain --bind /tmp:/tmp --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs /eos/home-a/areimers/slc6_latest.sif
