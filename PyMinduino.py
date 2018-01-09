import socket,json,time
import serial.tools.list_ports
import atexit


######socket creation

#print data
#print formatt

#r = neuroSocket.send(data)
#print r

def connectToNeurosky():
    neuroSocket = socket.create_connection(("127.0.0.1",13854))
    data = '{"appName":"appName","appKey":"appKey"}'
    formatt = '{"enableRawOutput":true,"format":"Json"}'
    r = neuroSocket.sendall(formatt)
    print r

    return neuroSocket

def main():
    try:
        #connectToNeurosky()

        print "Waiting for MindWave"
        neuroSocket = connectToNeurosky()
        if(neuroSocket != None):
            print "Connected to Neurosky MindWave"

        #connectToArduino()
        print "Connecting to Arduino"
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print p
            if("Silicon" or "Arduino" in p[1]):
                print "Arduino Located at ",p[0]
                ser = serial.Serial(p[0], 9600)
                hile ser.read() != '1':
                ser.read()
                print "arduino setup"

                ######30 sec delay
                print "wait for 30 sec ....."
                start=time.time()
                diff=0
                while diff<30:
                    rep = neuroSocket.recv(1024)
                    diff=time.time()-start
                    
        #receiveData()
        #######actual execution    
        fwd="1" 
        timeDiff=0
        start=time.time()

        while True:
            blinkc=0
            rep = neuroSocket.recv(1024)
            if("blink" in rep):
                print "blink"
                blinkc=blinkc+1
                #print rep
                rep = rep.split('\r')
                for data in rep:
                    print data
                    
            if("eSense" in rep):
                rep = rep.split('\r')
                for data in rep:
                    print data
            timeDiff=time.time()- start
            if timeDiff>3:
                print blinkc
                if blinkc==2:
                    fwd="2"
                    print("forward")
                else:
                    fwd="1"
                    print"stop"
                #ser.write(fwd.encode())
                timeDiff=0
                start=time.time()
                blinkc=0

            #print rep

    except KeyboardInterrupt:
        ser.close()
        neuroSocket.close()
        print "System Shutdown"
    finally:
        print "Clean up"


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
