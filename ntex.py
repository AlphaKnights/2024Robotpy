import sys
from networktables import NetworkTables as nt

def returnData(predictions):
    nt.getTable('Drive').getEntry('speedValueX', defaultvalue=1).setDouble(2) # replace with value
    nt.getTable('Drive').getEntry('speedValueY', defaultvalue=1).setDouble(2) # replace with value

def getData():
    # Replace with your actual data source or loading method
    distFront = nt.getTable('Drive').getValue(key='speedX', defaultValue=2)
    distBack = nt.getTable('Drive').getValue(key='speedY', defaultValue=2)
    distLeft = nt.getTable('Drive').getValue(key='distance', defaultValue=2)
    distRight = nt.getTable('Drive').getValue(key='distance', defaultValue=2)
    data=[distFront,distBack,distLeft,distRight]

def connectionListener(connected, info):
    print(info, f"; Connected={connected}")

# Initialized NT with RoboRIO IP
IP = sys.argv[1]
nt.initialize(server=IP)
# Tells if NT connectes to the RoboRIO
nt.addConnectionListener(connectionListener, immediateNotify=True)
nt.setUpdateRate(50) # ms

# Loop while
while True:
    continue