#!/usr/bin/env python
import os
import jenkinsapi


# get artifact for jobName
def downloadFromJenkins(url, jobName, user, pwd):
    path = os.environ['PWD'] + '/tmp'
    Artifact = jenkinsapi.api.get_latest_build(url, jobName, user, pwd)
    Art = str(Artifact)
# Build nr
    print 'Latest build number: ' + Art[Art.index('#') + 1:]
    buildnbr = Art[Art.index('#') + 1:]
# Job ID here is the same as build artifact
    jobid = 'jenkins-' + jobName + '-' + buildnbr + '.tar.bz2'
    print 'Jobid is: ' + jobid
# Download build
    print 'Downloading build'
    jenkinsapi.api.grab_artifact(
        url, jobName, jobid, path, user, pwd)
    return jobid


if __name__ == "__main__":
    # Delcaration
    url = 'http://10.8.16.62:8082'
    jobName = 'Test2'
    user = 'user'
    pwd = 'password'
    downloadFromJenkins(url, jobName, user, pwd)
