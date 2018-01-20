import socket,json,time
import serial.tools.list_ports
import sys
import serial

neuroSocket = None
ser = None

def connectToNeurosky():
    global neuroSocket
    neuroSocket = socket.create_connection(("127.0.0.1",13854))
    data = '{"appName":"appName","appKey":"appKey"}'
    formatt = '{"enableRawOutput":true,"format":"Json"}'
    r = neuroSocket.sendall(formatt)
    print "Device Response",r                     

    return r

def connectToArduino():
    global ser
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print p
        if("Silicon" in str(p[1]) or "Arduino" in str(p[1])):
            print "Arduino Located at ",p[0]
            ser = serial.Serial(p[0], 9600)
            break

def setupDevice():
    ######30 sec delay
    delay = 30
    print "Setting up device in "
    start=time.time()
    diff=0
    prevNum = delay
    while diff<delay:
        rep = neuroSocket.recv(1024)
        diff=time.time()-start
        currNum = int(delay-diff)
        if(prevNum != currNum):
            prevNum = currNum
            print currNum

def receiveData():
    isMoving = True
    fwd="1"
    stop = "2"
    timeDiff=0
    flag = 1
    blinkc=0
    while True:
        rep = neuroSocket.recv(1024)
        if("poor" in rep):
            rep = rep.split('\r')
            for data in rep:
                if("raw" in data or "mental" in data):                                  #skip unwanted values
                    continue
                if(len(data)>10):                                                       #avoid partial data, WIP
                    parsed_data=json.loads(data)
                    if('poorSignalLevel' in parsed_data):
                        if(parsed_data['poorSignalLevel'] > 0):
                            flag = 1
                            print "Poor Signal Detected. MindWave incorrectly placed."
                            print "Signal Strength :",parsed_data['poorSignalLevel']
                        else:
                            if(flag):
                                flag = 0
                                print "Connection Secured."
                    #if('blinkStrength' in parsed_data):
                    #    print "Blink Strength :",parsed_data['blinkStrength']
                    
        if("blink" in rep):
            if(blinkc == 0):
                start=time.time()
            print "blink"
            blinkc=blinkc+1
            print "Count :",blinkc
            if(blinkc == 2):
                timeDiff=time.time()- start
                print "Diff",timeDiff
                if timeDiff<=1:                                 #1 sec interval for detecting 2 blinks
                    print "Two Blinks Detected ",blinkc
                    
                    if(isMoving):                               #previous moving (any direction) then stop
                        print "Stop"
                        #ser.write(stop)
                        #call GUI for selecting direction
                    else:                                       #call gui for selecting direction
                        #GUI functiont
                        pass
                    timeDiff = 0
                    blinkc = 0
                else:
                    print "No Blink"
                    blinkc = 0
        
        
#        if("eSense" in rep):
#            rep = rep.split('\r')
#            for data in rep:
#                print data


'''
        timeDiff=time.time()- start
        if timeDiff>3:
            print blinkc
            if blinkc==2:
                fwd="2"
                print("forward")
            else:
                fwd="1"
                print"stop"
            ser.write(fwd)
            timeDiff=0
            start=time.time()
            blinkc=0

##################################
#    time.sleep(15)
    print "Forward"
    ser.write(fwd)

    time.sleep(3)
    #msg = ser.read(ser.inWaiting())
    #print msg

    print "Stop"
    ser.write(stop)

    time.sleep(5)
    #msg = ser.read(ser.inWaiting())
    #print msg
'''


def main():
    try:
        global neuroSocket, ser
        
        #connect to neurosky mindwave
        print "Waiting for MindWave"
        deviceResp = connectToNeurosky()
        if(deviceResp != None and neuroSocket != None):                             #MindWave or ThinkGear not connected 
            print "Connected to Neurosky MindWave"
            #connect to arduino
            print "Connecting to Arduino"
            connectToArduino()
            #receive data
            if(ser != None):
                #wait for MindWave Device
                setupDevice()
                print "Connected to Arduino"
                receiveData()
            else:
                print "Arduino not available"
        else:
            print "Error connecting to MindWave"

    except KeyboardInterrupt:
        print "Program Terminated"
    except Exception:
        tb = sys.exc_info()
        print "Exception"
        print tb[1]
        if("actively refused" in str(tb[1])):
            print "ThinkGear is not running you dumb fuck!"
        
    finally:
        print "Clean up"
        if(ser != None):
            ser.close()
        if(neuroSocket != None):
            neuroSocket.close()
        print "System Shutdown"


if __name__ == '__main__':
    main()
'''
ser.close()
    if("attention" in rep):
        print "waves"
        rep = rep.split('\r')
        #print rep
        print "\n"
        for data in rep:
            print data
            #parsed_data=json.loads(data)            #parsed_data is dict
            #print parsed_data
            #print "poor",parsed_data['poorSignal']
            #print "attention",parsed_data['eSense'][0]['attention']
    #time.sleep(2)



timeDiff=0
flag=1
while True:
    blinkc=0
    start=time.time()
    while timeDiff<1:
        rep = neuroSocket.recv(1024)
        if("blink" in rep):
            print "p"
            blinkc=blinkc+1
        timeDiff=time.time()- start
        #print timeDiff
    timeDiff=0
    print "blink :", blinkc
    #flag=int(raw_input())
   


        if("blink" in rep):
             print "blink2"
        else:
            print "blink1"
        time.sleep(1)
        print rep
        #time.sleep()
    #if("poor" in rep):
    #        print "Waves"
    #        print rep
    #print "START"
    #print rep.split('\r')
    #print "END"
'''
