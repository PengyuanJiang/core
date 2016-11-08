#!/usr/bin/env python 

# A 'Shell Call' is a shell call (duh) that we want to be reproduceable in the event of a failure. 
# namely, something that a developer can go in and 'drill in' on without running the entirety of the 
# build again.

import os
from subprocess import check_call
from subprocess import CalledProcessError
from os import path

def ShellCall(cmd, cwd = None):
    if not cwd:
        cwd = os.getcwd()

    try:
        check_call(cmd, shell=True, cwd=cwd)

    except CalledProcessError as repro_data:
        repro_filename = 'shellcall_failure-repro.sh'
        repro_destination = path.join(cwd, repro_filename)

        # when the call fails, print a repro to the working directory.
        with open(repro_destination, 'w') as repro_file:
            repro_file.writelines(['#!/usr/bin/env bash\n', repro_data.cmd + '\n'])

        # if we're rooted    
        if os.getuid() == 0:
            call('chmod +x %s'%(repro_filename), shell=True, cwd=cwd)

        # prints "Rover has detected a failure"
        print("a reproduction script was placed at : %s"%(repro_destination))
        print("To reproduce the failure:\n\tcd %s\n\t./%s"%(cwd, repro_filename))

        os._exit(1) # if we fail a check_call then we want to bail out asap so the dev can investigate.