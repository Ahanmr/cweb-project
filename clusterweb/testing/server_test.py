#!/bin/env/python3
#-*- encoding: utf-8 -*-
"""
===============================================================================
OSC Server
===============================================================================

-------------------------------------------------------------------------------
"""
from __future__ import print_function
from __future__ import division
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import numpy as np
import cloudpickle
import threading
import pickle
import zlib
import cv2
import sys
import os
import re


"""
===============================================================================
OSC Client Object
===============================================================================
"""

class OSCClient(object):

    def __init__(self,host,port):
        if not (re.match(r'^((\d){1,3}.){3}(\d{1,3})$',host,re.M|re.I)):
            raise Exception("Invalid host argument:{}".format(host))
        if not isinstance(port,int):
            raise Exception("Invalid port type:{}".format(
                type(port).__name__))
        if not (port >= 0 and port < 65535):
            raise Exception("Invalid port range (0-65535): {}".format(port))
        self.host = host
        self.port = port

    #--------------------------------------------------------------------------

    def init_client(self):
        self.client = udp_client.SimpleUDPClient(self.host,self.port)

    #--------------------------------------------------------------------------

    def send_data(self,data,channel="/machine1_server"):
        self.client.send_message(channel,data)

"""
===============================================================================
OSC Server Object
===============================================================================
"""

i = 1

def handle(channel,data):
    global i
    global client
    fnc = pickle.loads(data)
    data = fnc(i)
    client.send_data(data)
    i += 1

"""
===============================================================================
Job Object
===============================================================================
"""

class Job(obejct):

    def __init__(self,fnc,args,job_id,priority=None):
        self.fnc = fnc
        self.args = args
        self.job_id = job_id
        self.priority = priority
        self.output = None

    #--------------------------------------------------------------------------

    def run(self,in_thread=False):
        try:
            self.output = self.fnc(self.args)
        except Exception as e:
            self.output = e
        return self.output

    #--------------------------------------------------------------------------

    def run_thread(self):
        job_thread = threading.Thread(target=self.run,args=())
        job_thread.daemon = True
        job_thread.start()

    #--------------------------------------------------------------------------

    def compress(self,data):
        if isinstance(data,str):
            return pickle.dumps(data)

    #--------------------------------------------------------------------------

    def return_compressed(self):
        data = self.run()
        return self.compress(data)

"""
===============================================================================
OSC Server Object
===============================================================================
"""

class OSCServer(object):

    def __init__(self,host,port):
        if not (re.match(r'^((\d){1,3}.){3}(\d{1,3})$',host,re.M|re.I)):
            raise Exception("Invalid host argument:{}".format(host))
        if not isinstance(port,int):
            raise Exception("Invalid port type:{}".format(
                type(port).__name__))
        if not (port >= 0 and port < 65535):
            raise Exception("Invalid port range (0-65535): {}".format(port))
        self.host = host
        self.port = port
        self.jobs = []

    #--------------------------------------------------------------------------

    def init_server(self,handle):
        self.handler = dispatcher.Dispatcher()
        self.handler.map("/machine",handle)
        self.server = osc_server.ThreadingOSCUDPServer(
            (self.host,self.port),self.handler)

    #--------------------------------------------------------------------------

    def listen(self):
        self.server.serve_forever()

    #--------------------------------------------------------------------------

    def activate_listen_thread(self):
        self.listen_thread = threading.Thread(target=self.listen,args=())
        self.listen_thread.daemon = True
        self.listen_thread.start()

#------------------------------------------------------------------------------

def main():
    global client
    server_host = "127.0.0.1"
    client2server_port = 5006
    test_port = 5005
    client = OSCClient(server_host,client2server_port)
    client.init_client()
    server    = OSCServer(server_host,test_port)
    server.init_server(handle)
    server.listen()

if __name__ == "__main__":
    main()