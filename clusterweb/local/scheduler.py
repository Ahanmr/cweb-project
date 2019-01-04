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

        self.init_flag = True

        self.ip_address = self.fetch_ip_address()

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

    def init_handel(self,message):
        message = message.split(':')
        worker_id = message[1]
        port_num = message[2]

    #--------------------------------------------------------------------------

    def heartbeat(self):
        while True:

            self.head_socket = self.create_heartbeat_socket()
            if self.init_flag:
                message = 'I:{}'.format(self.worker_id)

                self.init_flag = False
                
            else:
                message = 'H:{}:{}'.format(self.worker_id,time.time())

            #print('Creating heartbeat message, ',message)
            self.head_socket.send_string(message)
            head_message = self.head_socket.recv()

            self.head_socket.close()
            time.sleep(1)


"""
===============================================================================

===============================================================================
"""

class WorkerData(object):

    def __init__(self,addr=None,port=None,worker_id=None,
            resources=None,excl=None,worker_num=None):
        self.addr = addr
        self.port = port
        self.worker_id = worker_id
        self.worker_num = worker_num
        self.resources = resources

        assert isinstance(config.NUM_HEARTBEATS,int)
        self.heartbeats = config.NUM_HEARTBEATS
        

"""
===============================================================================

===============================================================================
"""

# Server

class SchedulerHead(Scheduler):

    def __init__(self,
            head_addr=config.DEFAULT_HEAD_ADDRESS,
            head_port=config.DEFAULT_HEAD_PORT):
        super().__init__(head_addr=head_addr,head_port=head_port)
        self.head_addr = head_addr
        self.head_port = head_port

        self.n_workers = 0
        self.worker_ips = []
        self.worker_ids = []
        self.workers_data = {}

        self.ports = [self.head_port]

        self.head_socket = self.create_head_socket([self.head_port])

        self.handels = {'I':self.init_handel,'H':self.heartbeat_handel}

        #Process(target=self.heartbeat,args=()).start()

    #--------------------------------------------------------------------------

    def create_head_socket(self,ports):
        context = zmq.Context()
        head_socket = context.socket(zmq.REP)

        head_socket.bind('tcp://{}:{}'.format('*',self.head_port))

        return head_socket

    #--------------------------------------------------------------------------

    def init_handel(self,message):
        message = message.split(':')
        worker_id = message[1]

        if not worker_id in self.worker_ids:
            self.n_workers += 1
            self.print_log("New worker: {}".format(worker_id))
            w = WorkerData(worker_id=worker_id,worker_num=self.n_workers)
            self.workers_data[worker_id] = w
            self.worker_ids.append(worker_id)

        worker_message = 'I:{}:{}'.format(worker_id,
            self.head_port+self.n_workers)
        return worker_message

    #--------------------------------------------------------------------------

    def heartbeat_handel(self,message):
        message = message.split(':')
        worker_id = message[1]

        if not worker_id in self.worker_ids:
            raise Warning("Unknown worker: {}".format(worker_id))

        worker_num = self.workers_data[worker_id].worker_num

        self.print_log("Recieved heartbeat from worker: {}".format(worker_num))

        return 'h'

    #--------------------------------------------------------------------------

    def heartbeat(self):
        while True:
            print('waiting for heartbeat')

            message = self.head_socket.recv().decode()

            if message[0] in self.handels.keys():
               worker_message = self.handels[message[0]](message)
            else:
                raise Warning("Invalid message: {}".format(message))

            self.head_socket.send_string(worker_message)

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
        sh.heartbeat()
    else:
        sw = SchedulerWorker(head_addr=addr,head_port=port)
        sw.heartbeat()

if __name__ == "__main__":
    main()















