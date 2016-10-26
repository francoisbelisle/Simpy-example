#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "francois belisle"
__email__ = "f@mathmobile.io"

# A simple example of discret traffic signal event simulation using Simpy.
# The events in this simulation consist of : 
# - cars arriving
# - traffic signal changing states
# - Building, interrupting and relieving the traffic queues as they form.

# The story goes a little something like this :
# Cars send a message to the traffic controler when they arrive
# Depending on its state, the traffic controler either:
# - let's the car go (it's green for the cars movement)
# - Puts the car in a queue (if there already is a queue or if it's red)

# In this example, the traffic signal has two states:
# - a 15 second WBT
# - a 45 second SBT
# Both flows for the WBT and SBT movements are poissonly generated
# about every 10 seconds.
# Of course, all values should be changed to more realistic settings

# usage : python simpy-example.py

import random
from collections import deque
import simpy
RANDOM_SEED = 42
SIM_TIME = 120
LEAVE_CST = 3 

class BroadcastPipe(object):
    """
    A Broadcast pipe that allows one process to send messages 
    Taken from :
    http://simpy.readthedocs.io/en/latest/examples/process_communication.html
    """
    def __init__(self, env, capacity=simpy.core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def put(self, value):
        if self.pipes:
            events = [store.put(value) for store in self.pipes]
            return self.env.all_of(events)  

    def get_output_conn(self):
        pipe = simpy.Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe

    def remove_conn(self, pipe):
        self.pipes.remove(pipe)

class Flow(object):
    def __init__(self, env, out_pipe, mvt, interval):
        self.env = env
        self.out_pipe = out_pipe
        self.mvt = mvt
        self.interval = interval
        env.process(self.generate())

    def generate(self):
        i = 0
        while True:
            i += 1
            t = random.expovariate(1.0 / self.interval)
            yield self.env.timeout(t) 
            self.out_pipe.put((self.env.now, i, self.mvt))

class TrafficControler(object):
    def __init__(self, name, env, bc_pipe, timings=[], offset=0):
        self.env = env
        self.name = name
        self.bc_pipe = bc_pipe
        self.in_pipe = bc_pipe.get_output_conn()
        self.timings = timings
        self.offset = offset
        env.process(self.traffic_monitor()) 
        env.process(self.state())
        
        self.popqueue_proc = {}
        for mvt in timings : 
            self.popqueue_proc[mvt[0]] = env.process(self.pop_queue(mvt[0]))

        self.popqueue_proc_reactivate = {}
        for mvt in timings : 
            self.popqueue_proc_reactivate[mvt[0]] = env.event() 
        
        self.mvt = timings[0][0]

        self.queues = {} 
        for mvt in timings : 
            self.queues[mvt[0]] = deque()

    def state(self):
        self.mvt = self.timings[0][0]
        print("time %d : TRAFFIC STATE CHANGING %s" % (self.env.now, self.mvt))
        while True:
            i = 0
            k = len(self.timings)
            while i < len(self.timings):
                j = i + 1
                if j == k:
                    j = 0
                cur_mvt = self.timings[i][0]
                next_mvt = self.timings[j][0]
                self.mvt = yield self.env.timeout(self.timings[i][1], 
                                                  next_mvt)

                print("time %d : TRAFFIC STATE CHANGING %s" % 
                      (self.env.now, self.mvt))
                #if the queue is still poppin', we be interruptin'
                if self.popqueue_proc[cur_mvt].target.triggered:
                    if self.popqueue_proc[cur_mvt].target.value == "timingout":
                        self.popqueue_proc[cur_mvt].interrupt("changing phase")
                
                self.popqueue_proc_reactivate[next_mvt].succeed() 
                self.popqueue_proc_reactivate[next_mvt] = self.env.event()
                i += 1

    def traffic_monitor(self):
        while True:
            msg = yield self.in_pipe.get() # car arrivals
            print ("time %d : car %d %s has arrived" % 
                   (self.env.now, msg[1], msg[2]))
            if self.mvt == msg[2] and len(self.queues[msg[2]]) == 0:
                print("time %d : car %d %s has left" % 
                      (self.env.now, msg[1], msg[2]))
            else:
                self.queues[msg[2]].append(msg)
                print("time %d : car %d %s in queue" % 
                      (self.env.now, msg[1], msg[2]))
            
    def pop_queue(self, mvt):
        while True:
            yield self.popqueue_proc_reactivate[mvt]
            interrupted = False
            while len(self.queues[self.mvt]) > 0 and interrupted == False: 
                try:
                    yield self.env.timeout(LEAVE_CST*random.uniform(0.5, 1.5), 
                                           value="timingout") 
                    msg = self.queues[mvt].popleft()
                    print("time %d : car %d %s has left" % 
                          (self.env.now, msg[1], msg[2]))
                except simpy.Interrupt as i:
                    interrupted = True

if __name__ == '__main__':
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    bc_pipe = BroadcastPipe(env)

    signal = TrafficControler('Signal A', env, bc_pipe, [("WBT", 15), 
                                                      ("SBT", 45)])
    f1 = Flow(env, bc_pipe, "WBT", 10)
    f2 = Flow(env, bc_pipe, "SBT", 10)
    env.run(until=SIM_TIME)
