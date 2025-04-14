# truth-nano

Set up in CMSSW_14_1_0_pre4.
```
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

Initialize grid proxy
```
voms-proxy-init -voms cms
```

Submit crab job
```
cd dollar
crab submit crab_submit_EWKZToQQ.py
```

Check status of crab job
```
crab status crab/EWKZToQQ
```

Check here for exit codes of failed jobs: https://twiki.cern.ch/twiki/bin/viewauth/CMSPublic/JobExitCodes



