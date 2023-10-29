import os
import time

# Base
os.system('python -m pip install robotpy')
os.system('python -m pip install wpilib')
os.system('python -m pip install pyfrc')
os.system('python -m pip install pynetworktables')
os.system('python -m pip install robotpy[commands2]')
os.system('python -m pip install robotpy[ctre]')
os.system('python -m pip install robotpy[navx]')
os.system('python -m pip install robotpy[photonvision]')
os.system('python -m pip install robotpy[rev]')
# Extra
os.system('python -m pip install robotpy[pathplannerlib]')
os.system('python -m pip install robotpy[playingwithfusion]')
os.system('python -m pip install coverage')
os.system('python -m pip install opencv-python')
os.system('python -m pip install pillow')
os.system('python -m pip install tensorflow')

print('Window closing in 3 seconds...')
time.sleep(3)