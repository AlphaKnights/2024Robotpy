
"""
Recources:

[WPILib API Docs](https://robotpy.readthedocs.io/projects/wpilib/en/stable/wpilib.html)
[CommandsV2 API Docs](https://robotpy.readthedocs.io/projects/commands-v2/en/stable/api.html#command-v2-api)
[Getting Started](https://robotpy.readthedocs.io/en/stable/guide/anatomy.html#create-your-robot-code)

[Example Robot (Arm, CommandV2)](https://github.com/robotpy/examples/tree/main/commands-v2/armbot)
[UNOFFICIAL Swerve Example](https://github.com/Aurobots7456/SwerveDrive)
[Apriltag Package](https://robotpy.readthedocs.io/projects/apriltag/en/stable/robotpy_apriltag.html)
[Swerve Template JAVA](https://github.com/REVrobotics/MAXSwerve-Java-Template)
"""

import wpilib
import wpilib.drive
import commands2
from RobotContainer import RobotContainer

""" UNUSED LIBRARIES
import wpimath
import wpiutil
import robotpy
import pyfrc
import ctre
import navx
import rev
import pathplannerlib as ppl
import photonvision as phv
from Constants import NeoMotorConstants, DriveConstants, ModuleConstants, OIConstants, AutoConstants
"""


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # Instantiating our RobotContainer will perform all our button bindings, and put our
        # autonomous selection on the dashboard.
        self.container = RobotContainer()
        self.autonomousCommand = None

    def autonomousInit(self) -> None:
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def teleopInit(self) -> None:
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

    def testInit(self) -> None:
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(Robot)
    


"""
class Robot(commands2.TimedCommandRobot):

	def robotInit(self):
		#This function is called upon program startup. Main use is for initializing.
        
		self.gyro = navx.AHRS(2)
		self.DriveSystem = Drive()
		self.Constants = Constants()
		self.timer = wpilib.Timer()

	def autonomousInit(self):
		# This function is run once each time the robot enters autonomous mode.
		self.timer.reset()
		self.timer.start()


	def autonomousPeriodic(self):
		# This function is called periodically during autonomous.
		onStation = False
		decrease = 2.5
		lastAngle = 0.0

		pitch = self.gyro.getPitch()
		navXx = 0.0
		navXRot = pitch
		navXy = self.gyro.getDisplacementY()

		print(pitch)

		if (onStation):
			if (abs(pitch) > 2):
				speed = pitch / abs(pitch) / decrease
			else:
				speed = 0

			if (abs(pitch) > 2 and not(abs(lastAngle > 2))):
				decrease *= 2

			if ((abs(pitch) > 2 and docked)):
				docked = False 
				self.timer.stop()
				self.timer.reset()
			elif (abs(pitch) < 2):
				docked = True
				self.DriveSystem.move(0, 0, 0)

			self.DriveSystem.move(speed, 0, 0)

		elif (not onStation):
			if (abs(pitch) < 10):
				self.DriveSystem.move(0.2, 0, 0)
			else:
				onStation = True 

		lastAngle = pitch
	
	def teleopPeriodic(self):
		# This function is called periodically during operator control.

		self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())
"""