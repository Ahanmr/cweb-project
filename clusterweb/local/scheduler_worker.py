#!/usr/bin/env python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
from  multiprocessing import Process
import numpy as np 
import multiprocessing
import argparse
import psutil
import socket
import time
import tqdm
import sys
import re
import os

import config

#import clusterweb.local.config as config

import numpy as np
import base64
import zlib
import cv2
import sys
import zmq

"""
===============================================================================

===============================================================================
"""

class Scheduler(object):

    def __init__(self,
            head_addr=config.DEFAULT_HEAD_ADDRESS,
            head_port=config.DEFAULT_HEAD_PORT):

        assert isinstance(head_addr,str),('Invalid head_add type {}'.format(
            type(head_addr).__name__))

        re_check = re.search("((\d{1,3}.){3}\d)",head_addr)
        if re_check == None:
            raise UserWarning("Invalid server arg: {}".format(head_addr))
        # try:
        #     socket.inet_aton(socket.gethostbyname(head_addr))
        # except socket.error:
        #     raise UserWarning("Invalid head_addr arg: {}".format(head_addr))

        assert isinstance(head_port,int),('Invalid head_port type {}'.format(
            type(head_port).__name__))
        
        assert isinstance(head_addr,str),(
            'Invalid head_addr type: {}'.format(
            type(head_addr).__name__))

        assert re_check.group() == head_addr,(
            "Invalid server: {}".format(head_addr))

    #--------------------------------------------------------------------------

    def print_log(self,message,mode="INFO"):
        print('{} | {} | {}'.format(mode,time.ctime(),message),file=sys.stderr)

"""
===============================================================================

===============================================================================
"""

# Client


class SchedulerWorker(Scheduler):

    def __init__(self,
            head_addr=config.DEFAULT_HEAD_ADDRESS,
            head_port=config.DEFAULT_HEAD_PORT):
        super().__init__(head_addr=head_addr,head_port=head_port)

        self.worker_id = 'W_{}'.format(''.join(str(time.time()).split('.')))

        self.head_addr = head_addr
        self.head_port = head_port
        self.client_alive = []
        self.client_paths = []
        self.mode = 'local'
        self.n_jobs = 0

        self.init_flag = True

        self.ip_address = self.fetch_ip_address()

        self.messsage_handles = {'I':self.init_handle,
            'H':self.heartbeat_handle}

    #--------------------------------------------------------------------------

    def get_resources_status(self):
        ### FIX
        vm = psutil.virtual_memory()
        avail_vm = vm.available
        perc_vm = vm.percent

    #--------------------------------------------------------------------------

    def fetch_mode(self):
        if self.mode == None:
            ip = socket.gethostbyname(socket.gethostname())
            if ip != self.head_addr:
                self.mode = 'dist'
            else:
                self.mode = 'local'
        return self.mode

    #--------------------------------------------------------------------------

    def create_worker_socket(self):
        context = zmq.Context()
        worker_socket = context.socket(zmq.REP)

        worker_socket.bind('tcp://{}:{}'.format('*',self.worker_port))

        return worker_socket

    #--------------------------------------------------------------------------

    def create_heartbeat_socket(self,wait=True,wait_time=1.,timeout=60.):
        context = zmq.Context()
        head_socket = context.socket(zmq.REQ)
        print("tcp://localhost:{}".format(self.head_port))
        start_time = time.time()

        while (time.time()-start_time) <= timeout:
            try:
                head_socket.connect("tcp://localhost:{}".format(self.head_port))
                break
            except:
                time.sleep(wait_time)

        print("binding to tcp://{}:{}".format(self.head_addr,self.head_port))
        return head_socket

    #--------------------------------------------------------------------------

    def fetch_ip_address(self):
        if self.mode != 'local':
            return socket.gethostbyname(socket.gethostname())
        else:
            return '{}'.format(self.head_addr)

    #--------------------------------------------------------------------------

    def init_handle(self,message):
        self.worker_id = message[1]
        self.worker_port = message[2]

    #--------------------------------------------------------------------------

    def handle_head_message(self,message):
        message = message.split(':')
        header = message[0]
        response = self.messsage_handles[header](message)
        return response

    #--------------------------------------------------------------------------

    def heartbeat(self):
        while True:

            self.head_socket = self.create_heartbeat_socket()
            if self.init_flag:
                message = 'I:{}:{}'.format(self.worker_id,self.ip_address)

                self.init_flag = False
                
            else:
                message = 'H:{}:{}'.format(self.worker_id,time.time())

            #print('Creating heartbeat message, ',message)
            self.head_socket.send_string(message)

            head_message = self.head_socket.recv()
            response     = self.handle_head_message(head_message)

            self.head_socket.close()
            time.sleep(0.1)
        

"""
===============================================================================

===============================================================================
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode',required=False,type=str,
        default='h')

    parser.add_argument('--server',required=False,type=str,
        default='{}:{}'.format(config.DEFAULT_HEAD_ADDRESS,
            config.DEFAULT_HEAD_PORT))

    args = parser.parse_args()

    re_check = re.search("((\d{1,3}.){3}\d:\d{1,5})", args.server)
    if re_check == None:
        raise UserWarning("Invalid server arg: {}".format(args.server))

    addr,port = args.server.split(':')
    port = int(port)

    if args.mode == 'h':
        sh = SchedulerHead(head_addr=addr,head_port=port)
        #sh.heartbeat()
    else:
        sw = SchedulerWorker(head_addr=addr,head_port=port)
        sw.heartbeat()

if __name__ == "__main__":
    main()















