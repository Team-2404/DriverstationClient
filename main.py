import networktables
from networktables import NetworkTables
#from pynput.keyboard import Key, Listener
import keyboard
import threading
# As a client to connect to a robot
# def on_press(key):
#     print('{0} pressed'.format(
#         key))

# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()
cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.24.4.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()
keyin=NetworkTables.getTable("keyin")
keyin.putBoolean("keyQ",False)
keyinLocal=False
while True:
    try:
         if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            if not keyinLocal:
                print('You Pressed A Key!')
                keyin.putBoolean("keyQ",True)
                keyinLocal=True
         elif keyinLocal:
            keyin.putBoolean("keyQ",False)
            keyinLocal=False
    except:
        keyin.putBoolean("keyQ", False)