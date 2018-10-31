#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
from pythonosc import dispatcher
from pythonosc import osc_server
import numpy as np
import subprocess
import threading
import random
import time
import sys
import os
import re

from cweb.pbs.cluster_functions import *

"""
===============================================================================

===============================================================================
"""

class OSCServer(object):

    def __init__(self,host,port):
        if not (re.match(r'^((\d){1,3}.){3}(\d{1,3})$',host,re.M|re.I)):
            if not (host == 'localhost'):
                raise Exception("Invalid host argument:{}".format(host))
        if not isinstance(port,int):
            raise Exception("Invalid port type:{}".format(
                type(port).__name__))
        if not (port >= 0 and port < 65535):
            raise Exception("Invalid port range (0-65535): {}".format(port))
        self.host = host
        self.port = port

    #--------------------------------------------------------------------------

    def init_server(self,handle):
        self.handler = dispatcher.Dispatcher()
        self.handler.map("/filter", handle)
        self.server = osc_server.ThreadingOSCUDPServer(
            (self.host,self.port),self.handler)

    #--------------------------------------------------------------------------

    def print_volume_handler(self,unused_addr,args,volume):
        print("VH [{0}] ~ {1}".format(args[0], volume))

    #--------------------------------------------------------------------------

    def print_compute_handler(self,unused_addr,args,volume):
        try:
            print("CH [{0}] ~ {1}".format(args[0], args[1](volume)))
        except ValueError:
            pass

    #--------------------------------------------------------------------------

    def listen(self):
        self.server.serve_forever()

    #--------------------------------------------------------------------------

    def activate_listen_thread(self):
        self.listen_thread = threading.Thread(target=self.listen,args=())
        self.listen_thread.daemon = True
        self.listen_thread.start()

"""
===============================================================================

===============================================================================
"""

client_script = '''
#!/bin/env/python
#-*- encoding: utf-8 -*-
"""
Remote OSC Client Object
"""
from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import sys
import os
import re

#------------------------------------------------------------------------------

class OSCClient(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port

    #--------------------------------------------------------------------------

    def init_client(self):
        self.client = udp_client.SimpleUDPClient(self.host,self.port)

    #--------------------------------------------------------------------------

    def send_data(self,data,channel="/filter"):
        self.client.send_message(channel,data)

#------------------------------------------------------------------------------

def main():
    client = OSCClient('localhost','{}')
    client.init_client()
    while True:
        client.send_data(str(time.time()))
        time.sleep(1.0)

main()

'''

"""
===============================================================================

===============================================================================
"""

class SSH():

    def __init__(self,host):
        self.port=None
        self.set_address(host,self.port)

    #--------------------------------------------------------------------------

    def ssh_exists(self):
        """
        A method's docstring with parameters and return value.
        
        Use all the cool Sphinx capabilities in this description, e.g. to give
        usage examples ...
        
        :Example:

        >>> another_class.foo('', AClass())        
        
        :param arg1: first argument
        :type arg1: string
        :param arg2: second argument
        :type arg2: :class:`module.AClass`
        :return: something
        :rtype: string
        :raises: TypeError
        """
        try:
            subprocess.Popen(["ssh"],shell=False,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False



    #--------------------------------------------------------------------------

    def set_address(self,host,port):
        """
        A method's docstring with parameters and return value.
        
        Use all the cool Sphinx capabilities in this description, e.g. to give
        usage examples ...
        
        :Example:

        >>> another_class.foo('', AClass())        
        
        :param arg1: first argument
        :type arg1: string
        :param arg2: second argument
        :type arg2: :class:`module.AClass`
        :return: something
        :rtype: string
        :raises: TypeError
        """
        #if self.legal_address(host,port):  # FIX!!!
        self.host = host
        self.port = port
        #else:
        #    raise Exception("Invalid ssh argument: {}:{}".format(host,port))


    #--------------------------------------------------------------------------

    def legal_address(self,host,port):
        """ 

        """
        if not (re.match(r'^((\d){1,3}.){3}(\d{1,3})$',host,re.M|re.I)):
            if not (host == 'localhost'):
                return False

        if port != None:
            if not isinstance(port,int):
                return False

            if not (port >= 0 and port < 65535):
                return False

        return True


    #--------------------------------------------------------------------------

    def send_command(self,command):
        """ 

        """
        if not isinstance(command,str):
            raise Exception("Invalid command arg type: {}".format(
                type(command).__name__))

        if 'python ' in command:
            subprocess.call(['ssh',
                self.host,
                'python',command.split(' ')[1]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE) # FIX!!!
            result = None

        else:

            ssh_output = subprocess.Popen(["ssh","%s"%self.host,command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)

            result = ssh_output.stdout.readlines()
            for i,n in enumerate(result):
                result[i] = n.decode()[:-1]

        return result

    #--------------------------------------------------------------------------

    def send_file(self,origin_path,destination_path):
        """ 

        """
        if not os.path.exists(origin_path):
            raise Exception("Invalid origin_path: {}".format(
                origin_path))

        scp = subprocess.Popen(["scp","{}".format(origin_path),
            "{}:{}".format(self.host,destination_path)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
        result = scp.stdout.readlines()

    #--------------------------------------------------------------------------

    def send_folder(self,origin_dir,destination_dir):
        """ 

        """
        if not os.path.exists(origin_dir):
            raise Exception("Invalid origin_path: {}".format(
                origin_path))

        if not os.path.isdir(origin_dir):
            raise Exception("Directory arg invalid: {}".format(
                origin_reipath))

        scp = subprocess.Popen(["scp",'-r',"{}".format(origin_dir),
            "{}:{}".format(self.host,destination_dir)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)

        result = scp.stdout.readlines()

    #--------------------------------------------------------------------------

    def recieve_file(self,origin_path,destination_path):

        scp = subprocess.Popen(["scp","{}:{}".format(self.host,
            origin_path),"{}".format(destination_path)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
        result = scp.stdout.readlines()
"""
===============================================================================

===============================================================================
"""

def login(ssh_name):
    """
    A method's docstring with parameters and return value.
    
    Use all the cool Sphinx capabilities in this description, e.g. to give
    usage examples ...
    
    :Example:

    >>> login('colfax')        
    
    :param ssh_name: The keyword used to access a cluster
    :type ssh_name: string
    :raises: FileNotFoundError, UserWarning, Exception
    """

    dcf = DevCloudFunctions()

    if isinstance(ssh_name,str):
        if not ' ' in ssh_name:
            ssh_config_path = os.path.join(os.path.expanduser('~'),'.ssh/config')
            if not os.path.exists(ssh_config_path):
                raise FileNotFoundError("SSH Config file not found: {}".format(
                    ssh_config_path))

            valid = False
            with open(ssh_config_path,'r') as f:
                ssh_config = f.read()
                for n in ssh_config.split('\n'):
                    n = n.split(' ')
                    if n[0] == 'Host':
                        print(n[1])
                        if n[1] == ssh_name:
                            valid = True

            if not valid:
                raise UserWarning("{} not found in ssh config: {}".format(
                    ssh_name,ssh_config_path))


            if not dcf.can_access_devcloud(ssh_name):
                raise Exception("Cannot connect to DevCloud: {}".format(
                        ssh_name))

            with open(os.path.join(os.path.dirname(
                os.path.abspath(__file__)),'username.txt'),'w') as f:
                f.write(ssh_name)

"""
===============================================================================

===============================================================================
"""

def test():
    ssh = SSH('colfax',6006)
    ssh.test()


if __name__ == "__main__":
    test()













