"""


"""
from __future__ import print_function
from __future__ import division
import numpy as np
import cloudpickle
import subprocess
import threading
import random
import pickle
import shutil
import math
import time
import sys
import os
import re

from clusterweb.interfaces import ssh
from clusterweb.pbs import scripts
from clusterweb.pbs import config
from clusterweb.pbs import qstat

"""
===============================================================================

===============================================================================
"""

class Qsub():

    def __init__(self,target,args,
            n_nodes=config.DEFAULT_NODES,
            n_cores=config.DEFAULT_CORES,
            set_walltime=config.DEFAULT_WALLTIME,
            set_memory=config.DEFAULT_MEMORY,
            set_cpu=config.DEFAULT_CPU,
            wait_time=config.DEFAULT_WAIT_TIME,
            verbose=0):

        self.target = target
        self.args = args

        self.username = config.USERNAME
        self.ssh = ssh.SSH(self.username)

        self.fnc = cloudpickle.dumps(target)
        self.args = pickle.dumps(args)

        self.temp_dir = 'temp_{}{}'.format(
            ''.join(str(time.time()).split('.')),
            random.randint(10000,100000))

        # FIX: Allocate resource functions
        self.n_nodes        = n_nodes
        # Qsub script placeholder for number of cores
        self.n_cores        = n_cores
        # Qsub script placeholder for the walltime allocated
        self.set_walltime   = set_walltime
        self.allocate_walltime(self.set_walltime)

        # Qsub script placeholder for memory allocated
        self.set_memory     = set_memory
        # Qsub script placeholder for cpu time allocated
        self.set_cpu        = set_cpu

        self.wait_time = wait_time

        self.complete = False

        self.verbose = verbose

    #--------------------------------------------------------------------------

    def __lt__(self,job):
        """Sets the amount of walltime

        Will raise exception if str argument is not in the form hr:min:sec

        :param walltime: amount of walltime in seconds
        :type walltime: str, int, float

        :returns: None

        :Example:

        >>> q.allocate_walltime('0:05:00') # Five minutes
        >>> q.allocate_walltime(600) # Ten minutes
        >>> q.allocate_walltime(599.6) # Rounds to ten minutes

        .. note:: The walltime configuration can be adjusted by admins in 
            `devcloud/devcloud_config.py`.

        .. warning:: If users adjust `devcloud/devcloud_config.py` to
            settings not authorized by cluster admins, it will raise
            errors on the cluster and the job will not be submitted.
        """
        data = qstat.Qstat()



        if self.qstat_update:





    #--------------------------------------------------------------------------

    def generate_qsub_script(self):
        """Return the PBS submission script from the specified resource
        allocations.

        :returns: None
        """
        return scripts.qscript.format(
            self.n_nodes,
            self.n_cores,
            self.set_walltime,
            self.set_memory,
            self.set_cpu,
            'python {}/pyscript.py'.format(self.temp_dir))



    #--------------------------------------------------------------------------

    def allocate_walltime(self,walltime):
        """Sets the amount of walltime

        Will raise exception if str argument is not in the form hr:min:sec

        :param walltime: amount of walltime in seconds
        :type walltime: str, int, float

        :returns: None

        :Example:

        >>> q.allocate_walltime('0:05:00') # Five minutes
        >>> q.allocate_walltime(600) # Ten minutes
        >>> q.allocate_walltime(599.6) # Rounds to ten minutes

        .. note:: The walltime configuration can be adjusted by admins in 
            `devcloud/devcloud_config.py`.

        .. warning:: If users adjust `devcloud/devcloud_config.py` to
            settings not authorized by cluster admins, it will raise
            errors on the cluster and the job will not be submitted.
        """
        if isinstance(walltime,(int,float)):
            walltime = str(datetime.timedelta(seconds=walltime))

        def intable(z):
            try:
                int(z)
                return True 
            except:
                return False

        if isinstance(walltime,str):
            split_exp = walltime.split(':')
            if np.all(list(map(intable,split_exp))) and len(split_exp) == 3:
                # TODO: Add config check
                pass
            else:
                raise Exception("Invalid walltime arg: {}".format(walltime))

        c = [3600,60,1]
        self.total_walltime = sum([int(A)*int(B) for A,B in zip(
            walltime.split(':'),c)])

        self.set_walltime = walltime

    #--------------------------------------------------------------------------

    def push(self):

        os.mkdir(self.temp_dir)

        with open(os.path.join(self.temp_dir,'fnc.pkl'),'wb') as f:
            f.write(self.fnc)

        with open(os.path.join(self.temp_dir,'args.pkl'),'wb') as f:
            f.write(self.args)

        with open(os.path.join(self.temp_dir,'pyscript.py'),'w') as f:
            f.write(scripts.pyscript.format(sys.version_info.major,self.temp_dir))

        with open(os.path.join(self.temp_dir,'qscript'),'w') as f:
            f.write(self.generate_qsub_script())

        self.ssh.send_folder(self.temp_dir,self.temp_dir)

        [self.job_id] = self.ssh.send_command('qsub {}'.format(os.path.join(
            self.temp_dir,'qscript')))

    #--------------------------------------------------------------------------

    def fetch_result(self):

        result_path = os.path.join(self.temp_dir,'result.pkl')

        while True:
            result = subprocess.check_output(
                'ssh colfax [ -f {} ] && echo "1" || echo "0"'.format(
                    result_path),stderr=subprocess.STDOUT,shell=True)

            if int(result[-2]) == 49:
                break
            else:
                time.sleep(self.wait_time)

        self.ssh.recieve_file(result_path,result_path)

        print(result_path)

        with open(result_path,'rb') as f:
            self.result   = pickle.loads(f.read())
            self.complete = True

        self.ssh.send_command('rm -rf {}'.format(self.temp_dir))
        self.ssh.send_command('rm qsub_script.*{}'.format(self.job_id.split('.')[0]))
        shutil.rmtree(self.temp_dir)
        
        
    #--------------------------------------------------------------------------

    def pull(self):
        result_thread = threading.Thread(target=self.fetch_result,args=())
        result_thread.start()

