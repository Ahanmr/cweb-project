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

from scheduler import Scheduler


"""
===============================================================================

===============================================================================
"""

class WorkerData(object):

    def __init__(self,addr=None,port=None,worker_id=None,
            resources=None,excl=None,worker_num=None,
            worker_addr=None):
        self.addr        = addr
        self.port        = port
        self.worker_id   = worker_id
        self.worker_num  = worker_num
        self.resources   = resources

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

        self.handles = {'I':self.init_handle,'H':self.heartbeat_handle}

        Process(target=self.heartbeat,args=()).start()

    #--------------------------------------------------------------------------

    def create_head_socket(self,port):
        context = zmq.Context()
        head_socket = context.socket(zmq.REP)

        head_socket.bind('tcp://{}:{}'.format('*',self.head_port))

        return head_socket

    #--------------------------------------------------------------------------

    def send_job(self,worker_id):
        pass


    #--------------------------------------------------------------------------

    def init_handle(self,worker2head_message):
        message     = worker2head_message.split(':')
        worker_id   = worker2head_message[1]
        worker_addr = worker2head_message[2]

        if not worker_id in self.worker_ids:
            self.n_workers += 1
            self.print_log("New worker: {}".format(worker_id))

            w = WorkerData(addr=worker_addr,
                worker_id=worker_id,
                worker_num=self.n_workers)

            self.workers_data[worker_id] = w
            self.worker_ids.append(worker_id)

        head2worker_message = 'I:{}:{}'.format(worker_id,
            self.head_port+self.n_workers)
        return head2worker_message

    #--------------------------------------------------------------------------

    def heartbeat_handle(self,message):
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

            worker2head_message = self.head_socket.recv().decode()

            if message[0] in self.handles.keys():
                head2worker_message = self.handles[worker2head_message[0]](
                    worker2head_message)
            else:
                raise Warning("Invalid message: {}".format(
                    worker2head_message))

            self.head_socket.send_string(head2worker_message)

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


if __name__ == "__main__":
    main()















