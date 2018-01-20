import socket,json,time,serial
import serial.tools.list_ports
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import QTimer,QTime
import sys
import gui
import threading


neuroSocket = None
ser = None
direction = 0
flag=0
counter=3
isMoving = False

class WheelchairControl(QtGui.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined    
        self.imageLabel.setFont(QtGui.QFont("Droid Sans",48,QtGui.QFont.Bold))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tick()
        

    def tick(self):
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.lcdDisplay)
        self.timer.start(1000)

    def change(self):
        print 'change'
        global isMoving, flag, direction 
        self.imageLabel.setFont(QtGui.QFont("Droid Sans",48,QtGui.QFont.Bold))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        #for color change
        #self.imageLabel.setStyleSheet("color: rgb(255,0,0)")
        print "Moving",isMoving
        print "Flag",flag
        if isMoving:
            self.currentCommand("Moving")           
            if direction==0:
                    self.imageLabel.setText("RIGHT")
                    #for image display
                    #self.imageLabel.setStyleSheet("image: url(:/Directions/images/right.jpg)")
            
            elif direction==1:
                self.imageLabel.setText("LEFT")
            
            else:
                self.imageLabel.setText("FORWARD")
            
        else:
                self.currentCommand("Stopped")
                if flag==0:
                    self.imageLabel.setText("RIGHT")
                    print "right selected"
                    direction = 0
                    flag=1
                elif flag==1:
                    self.imageLabel.setText("LEFT")
                    print "left selected"
                    direction = 1
                    flag=2
                else:
                    self.imageLabel.setText("FORWARD")
                    print "forward selected"
                    direction = 2
                    flag=0


    def lcdDisplay(self):
        global counter
        if counter==0:
            text=str(counter)
            self.lcdNumber.display(text)
            counter=3
            self.change()
        else:
           text=str(counter)
           counter-=1
           self.lcdNumber.display(text)

    def currentCommand(self, command):
        self.currentLabel.setFont(QtGui.QFont("Droid Sans",14,QtGui.QFont.Bold))
        self.currentLabel.setAlignment(QtCore.Qt.AlignCenter)
        #for color change
        self.currentLabel.setStyleSheet("color: rgb(85,0,255)")
        self.currentLabel.setText(command)
        
class Minduino:
    
    def setupHardware(self,stopEvent):
        global neuroSocket, ser

        #connect to neurosky mindwave
        print "Waiting for MindWave"
        self.connectToNeurosky()
        if(neuroSocket != None):
            print "Connected to Neurosky MindWave"
            #connect to arduino
            print "Connecting to Arduino"
            self.connectToArduino()
            #receive data
            if(ser != None):

                self.setupDevice(stopEvent)
                
                print "Connected to Arduino"
                
                self.receiveData(stopEvent)
            else:
                print "Arduino not available"
        else:
            print "Error connecting to MindWave"

    def connectToNeurosky(self):
        global neuroSocket
        neuroSocket = socket.create_connection(("127.0.0.1",13854))
        data = '{"appName":"appName","appKey":"appKey"}'
        formatt = '{"enableRawOutput":true,"format":"Json"}'
        r = neuroSocket.sendall(formatt)
        print "Device Response",r                     


    def connectToArduino(self):
        global ser
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print p
            if("Silicon" in str(p[1]) or "Arduino" in str(p[1])):
                print "Arduino Located at ",p[0]
                ser = serial.Serial(p[0], 9600)
                break

    def setupDevice(self, stopEvent):
        ######30 sec delay
        delay = 3
        print "Setting up device in "
        start=time.time()
        diff=0
        prevNum = delay
        while diff<delay and not stopEvent.is_set():
            rep = neuroSocket.recv(1024)
            diff=time.time()-start
            currNum = int(delay-diff)
            if(prevNum != currNum):
                prevNum = currNum
                print currNum

    def receiveData(self, stopEvent):
        print "recv"
        fwd="1"
        stop = "2"
        timeDiff=0
        flag = 1
        global isMoving, counter
        blinkc=0
        while not stopEvent.is_set():
            rep = neuroSocket.recv(1024)    
            '''
            if("poor" in rep):
                rep = rep.split('\r')
                for data in rep:
                    if("raw" in data or "mental" in data):                                  #skip unwanted values
                        continue
                    if(len(data)>10):                                                       #avoid partial data, WIP
                        #print data
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
            '''
            if("blink" in rep):
                if(blinkc == 0):
                    start=time.time()
                print "blink"
                blinkc=blinkc+1
                print "Count :",blinkc
                if(blinkc == 2):
                    
                    timeDiff=time.time()- start
                    print "Start",start
                    print "Diff",timeDiff
                    if timeDiff<=1:                                 #1 sec interval for detecting 2 blinks
                        print "Two Blinks Detected ",blinkc
                        
                        if(isMoving):                               #previous moving (any direction) then stop
                            print "Stop"
                            counter = 1
                            #self.imageLabel.setText("STOP")
                            #ser.write(stop)
                            isMoving = False
                        else:                                       #call gui for selecting direction
                            #GUI function
                            isMoving = True
                            #self.change()
                            pass
                        timeDiff = 0
                        blinkc=0
                    else:
                        print "No Blink"
                        blinkc=0


    #        if("eSense" in rep):
    #            rep = rep.split('\r')
    #            for data in rep:
    #                print data


def main():

        #open an instance of QApplication
        
        app = QtGui.QApplication(sys.argv)
        form = WheelchairControl()
        form.show()
        app.exec_()
        

if __name__ == '__main__':

    try:
        setup = Minduino()
        stopEvent = threading.Event()
        t = threading.Thread(target=setup.setupHardware,args=(stopEvent,))
        t.daemon = True
        t.start()

        main()
        
    except KeyboardInterrupt:
            print "Program Terminated"
    except Exception:
        tb = sys.exc_info()
        print "Exception"
        if("actively refused" in str(tb[1])):
            print "ThinkGear is not running you dumb fuck!"
        elif("COM" in str(tb[1])):
            print "COM Port is busy"
        else:
            print tb[1]

    finally:
        print "Clean up"
        stopEvent.set()
        if(ser != None):
            ser.close()
        if(neuroSocket != None):
            neuroSocket.close()
        print "System Shutdown"    

