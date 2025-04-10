from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.requestName = 'EWKWminusToQQ'
config.General.workArea = 'crab'
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'EWKWminusToQQ.py'
config.JobType.disableAutomaticOutputCollection = False
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 4700
config.JobType.numCores = 1
config.JobType.pyCfgParams = ['gridpack=./ewkwmjjjj_5f_LO_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz']

config.section_("Data")
config.Data.outputPrimaryDataset = 'EWKWminusToQQ'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 5000 #0
NJOBS = 200  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/jdickins/ewk-v-slash/'
config.Data.publication = True
config.Data.outputDatasetTag = 'EWKWminusToQQ'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
