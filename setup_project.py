import os
import time

# Base
os.system('cmd /c py -m pip install robotpy')
os.system('cmd /c py -m pip install wpilib')
os.system('cmd /c py -m pip install pyfrc')
os.system('cmd /c py -m pip install pynetworktables')
os.system('cmd /c py -m pip install robotpy[commands2]')
os.system('cmd /c py -m pip install robotpy[ctre]')
os.system('cmd /c py -m pip install robotpy[navx]')
os.system('cmd /c py -m pip install robotpy[photonvision]')
os.system('cmd /c py -m pip install robotpy[rev]')
# Extra
os.system('cmd /c py -m pip install robotpy[pathplannerlib]')
os.system('cmd /c py -m pip install robotpy[playingwithfusion]')
os.system('cmd /c py -m pip install coverage')
os.system('cmd /c py -m pip install opencv-python')
os.system('cmd /c py -m pip install pillow')
os.system('cmd /c py -m pip install tensorflow')

print('Window closing in 3 seconds...')
time.sleep(3)