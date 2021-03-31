# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 07:37:47 2018

@author: Aishwarya
"""

'''
import pandas as pd
import numpy as np
import os

api_key = "AIzaSyDW0RilIKPYk0TDWlLGdlLYobr77eqz3AQ"

'''
import threading
import time

validity_a = 20
validity_b = 25

req = 10


def loop_t1(t):
    print("In thread1")
    i = 1
    while(i<=t):
        if(req==0):
            print("Passenger request received in taxi1\n")
            break
        time.sleep(1)
        i += 1
    
def loop_t2(t):
    print("In thread2")
    i = 1
    while(i<=t):
        if(req==0):
            print("Passenger request received in taxi2\n")
            break
        time.sleep(1)
        i += 1

if __name__ == "__main__": 
    # creating thread 
    t1 = threading.Thread(target=loop_t1,args=(validity_a,)) 
    t2 = threading.Thread(target=loop_t2,args=(validity_b,)) 
  
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start()
    
    time.sleep(req)
    print("Passenger request now arrived")
    time.sleep(1)
    req = 0
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
  
    # both threads completely executed 
    print("Done!") 

