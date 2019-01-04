#!/bin/env/python3
#-*- encoding: utf-8 -*-
"""
===============================================================================
OSC Client
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
import argparse
import random
import pickle
import json
import time
import zlib
import sys
import os
import re

def handle(channel,data):
    print(data)

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

    #--------------------------------------------------------------------------

    def init_server(self,handle):
        self.handler = dispatcher.Dispatcher()
        self.handler.map("/machine1_server",handle)
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

    def send_data(self,data,channel="/machine"):
        self.client.send_message(channel,data)

#------------------------------------------------------------------------------

def test(arg):
    return np.sqrt(arg)

def main():
    host = "127.0.0.1"
    client_port = 5005
    server_port = 5006
    client    = OSCClient(host,client_port)

    server = OSCServer(host,server_port)

    server.init_server(handle)
    server.activate_listen_thread()

    client.init_client()
    while True:
        fnc = cloudpickle.dumps(test)
        client.send_data(fnc)

if __name__ == "__main__":
  main()