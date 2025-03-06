from networktables import NetworkTables
#from pynput.keyboard import Key, Listener
import keyboard
import threading

data={False,False,False,False,False,False,False,False,False}

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()
def released(key):
    data[key]=False
    keyin.putBooleanArray("keyArr",data)
def pressed(key):
    data[key]=True
    keyin.putBooleanArray("keyArr",data)

NetworkTables.initialize(server='10.24.4.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

keyin=NetworkTables.getTable("keyin")
keyin.putBooleanArray("keyQ",data)

keyboard.add_hotkey("a",lambda:pressed(),suppress=True)
keyboard.add_hotkey("a",lambda:released(),suppress=True,trigger_on_release=True)