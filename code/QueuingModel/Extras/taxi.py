from flask import Flask
import threading
import time


app = Flask(__name__)


taxi1 = {'id': 1, 'currentLoc': [41.877406123,-87.621971652], 'noPassengers':0, 'direction':[]}
taxi2 = {'id': 2, 'currentLoc': [41.898331794,-87.620762865], 'noPassengers':0, 'direction':[]}
i = 0
reqInterupt = 0
servInterupt1 = 0
servInterupt2 = 0
reqConfirmed1 = 0
reqConfirmed2 = 0
reqData1 = 
reqData2 = {}


################################################################################

def updateTaxiData1():
    global taxi1
    if(taxi1['noPassengers'] > 0):
        taxi1['currentLoc'] = taxi1['direction']['loc']
        taxi1['direction'].pop(0)
        if(len(taxi1['direction']) == 0):
            taxi1['noPassengers'] -= 1
    t1 = threading.Timer(10, updateTaxiData1)
    t1.start()

    
def updateTaxiData2():
    global taxi2
    if(taxi2['noPassengers'] > 0):
        taxi2['currentLoc'] = taxi2['direction']['loc']
        taxi2['direction'].pop(0)
        if(len(taxi2['direction']) == 0):
            taxi2['noPassengers'] -= 1
    
    t2 = threading.Timer(10, updateTaxiData1)
    t2.start()


def taxi_t1():
    global taxi1
    global reqInterupt
    global servInterupt1
    print("Taxi 1 started, Current Location: ",taxi1['currentLoc'])
    nextUpdate = 0
    t1 = threading.Timer(10, updateTaxiData1) 
    t1.start()
    while(1):
        if(reqInterupt == 1):
            #RUNACO
            servInterupt1 = 1
        if(reqConfirmed1 == 1):
            #updateTaxiData
            continue
        
def taxi_t2():
    global taxi2
    global reqInterupt
    global servInterupt2

    print("Taxi 2 started, Current Location: ",taxi2['currentLoc'])
    t2 = threading.Timer(10, updateTaxiData1) 
    t2.start()
    while(1):
        if(reqInterupt == 1):
            #RUNACO
            servInterupt2 = 1
        if(reqConfirmed2 == 1):
            #updateTaxiData
            continue
        



t1 = threading.Thread(target=taxi_t1)
t2 = threading.Thread(target=taxi_t2) 
  
    # starting thread 1 
t1.start() 
    # starting thread 2 
t2.start()

##################################################################


@app.route('/makeRequest')
def makeRequestToTaxi():
    global reqInterupt
    reqInterupt = 1
    if(servInterupt1 == 1 and servInterupt2 == 2):
        return([reqData1,reqData2])

@app.route('/ConfirmRequest')
def confrimRequestToTaxi():
    return()
    



if __name__ == '__main__':
    app.run()
       
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
  
    app.run()
    # both threads completely executed 
    print("Done!") 
