
"""
Recources:

[WPILib API Docs](https://robotpy.readthedocs.io/projects/wpilib/en/stable/wpilib.html)
[CommandsV2 API Docs](https://robotpy.readthedocs.io/projects/commands-v2/en/stable/api.html#command-v2-api)
[Getting Started](https://robotpy.readthedocs.io/en/stable/guide/anatomy.html#create-your-robot-code)

[Example Robot (Arm, CommandV2)](https://github.com/robotpy/examples/tree/main/commands-v2/armbot)
"""

import wpilib
import wpilib.drive
import commands2 as cmd2
import robotpy

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup. Main use is for initializing.
        """
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.drive.swerveDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())


if __name__ == "__main__":
    wpilib.run(MyRobot)