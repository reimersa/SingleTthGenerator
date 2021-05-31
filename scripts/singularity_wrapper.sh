#! /bin/bash

# first argument must be the executable, the remaining arguments are those passed to the executable

echo "before singularity"
echo $CMSSW_VERSION
cd $7 # CMSSW Path for Gridpacks to get PATH and includes right.
eval `scramv1 runtime -sh`
cd -
cat /etc/redhat-release
CMD="SINGULARITYENV_ClusterId=$ClusterId SINGULARITYENV_ProcId=$ProcId SINGULARITYENV_X509_VOMS_DIR=$X509_VOMS_DIR SINGULARITYENV_X509_CERT_DIR=$X509_CERT_DIR SINGULARITYENV_X509_USER_PROXY=$X509_USER_PROXY SINGULARITYENV_CMSSW_VERSION=$CMSSW_VERSION SINGULARITYENV_SCRAM_ARCH=$SCRAM_ARCH SINGULARITYENV_LD_LIBRARY_PATH=$LD_LIBRARY_PATH SINGULARITYENV_PREPEND_PATH=$PATH SINGULARITYENV_KRB5CCNAME=$KRB5CCNAME singularity exec --cleanenv --bind /tmp:/tmp --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs --bind /pool:/pool /eos/home-a/areimers/slc6_latest.sif $1 $2 $3 $4 $5 $6"
echo $CMD
eval $CMD

  # --bind /etc:/etc
  # --bind /usr:/usr --bind /lib64:/lib64 --bind /bin:/bin
