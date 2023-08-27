# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import math

from wpimath import units
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.trajectory import TrapezoidProfileRadians

from rev import CANSparkMax

from networktables import NetworkTablesInstance

from enum import Enum


class NeoMotorConstants:
	kFreeSpeedRpm = 5676
	kFreeSpeedRps = kFreeSpeedRpm / 60


class DriveConstants:
	# Maximum allowed speeds, not maximum possible speeds
	kMaxSpeedMetersPerSecond = 4.8
	kMaxAngularSpeed = math.tau  # radians per second

	kDirectionSlewRate = 1.2  # radians per second
	kMagnitudeSlewRate = 1.8  # percent per second (1 = 100%)
	kRotationalSlewRate = 2.0  # percent per second (1 = 100%)

	# Chassis configuration
	kTrackWidth = units.inchesToMeters(26.5)
	# Distance between centers of right and left wheels on robot
	kWheelBase = units.inchesToMeters(26.5)

	# Distance between front and back wheels on robot
	kModulePositions = [
		Translation2d(kWheelBase / 2, kTrackWidth / 2),
		Translation2d(kWheelBase / 2, -kTrackWidth / 2),
		Translation2d(-kWheelBase / 2, kTrackWidth / 2),
		Translation2d(-kWheelBase / 2, -kTrackWidth / 2),
	]
	kDriveKinematics = SwerveDrive4Kinematics(*kModulePositions)

	# Angular offsets of the modules relative to the chassis in radians
	kFrontLeftChassisAngularOffset = -math.pi / 2
	kFrontRightChassisAngularOffset = 0
	kBackLeftChassisAngularOffset = math.pi
	kBackRightChassisAngularOffset = math.pi / 2

	# SPARK MAX CAN IDs
	kFrontRightDrivingCanId = 5
	kFrontLeftDrivingCanId = 6
	kBackRightDrivingCanId = 7
	kBackLeftDrivingCanId = 8
	
	kFrontRightTurningCanId = 9
	kFrontLeftTurningCanId = 10
	kBackRightTurningCanId = 11
	kBackLeftTurningCanId = 12
	

	kGyroReversed = False


class ElevatorConstants:
    kSensorCountPerRevolution = 2048
    kDefaultMaxFowardVerticalRotation = 135
    kDefaultFowardVerticalCount = kDefaultMaxFowardVerticalRotation*kSensorCountPerRevolution
    kMaxReverseVerticalRotationCount = 0
    kElevatorFalconID = 3
    kReverseLimitSwitchPort = 0
    kForwardLimitSwitchPort = 1

    kP = 0.06277
    kI = 0
    kD = 0
    kF = 0.049286
    kIZone = 0

    kPeakOutput = 0.2

    kPositionTolerance = 0.1
    kElevatorLowPosition = 25
    kElevatorMidPosition = 50
    kElevatorHighPosition = 100


class ModuleConstants:
	# MAXSwerve modules can either have 12T, 13T, or 14T gearing (more teeth = more faster)
	kDrivingMotorPinionTeeth = 14

	# The output shaft rotates in the opposite direction of the steering motor in MAXSwerve Modules
	kTurningEncoderInverted = True

	# Calculations required for driving motor conversion factors and feed forward
	kWheelDiameterMeters = 0.0762
	kWheelCircumferenceMeters = kWheelDiameterMeters * math.pi
	# 45 teeth on the wheel's bevel gear, 22 teeth on the first-stage spur gear, 15 teeth on the bevel pinion
	kDrivingMotorReduction = (45.0 * 22) / (kDrivingMotorPinionTeeth * 15)
	kDriveWheelFreeSpeedRps = (
		NeoMotorConstants.kFreeSpeedRps * kWheelCircumferenceMeters
	) / kDrivingMotorReduction

	kDrivingEncoderPositionFactor = (
		kWheelDiameterMeters * math.pi
	) / kDrivingMotorReduction  # meters
	kDrivingEncoderVelocityFactor = (
		(kWheelDiameterMeters * math.pi) / kDrivingMotorReduction
	) / 60.0  # meters per second

	kTurningEncoderPositionFactor = math.tau  # radian
	kTurningEncoderVelocityFactor = math.tau / 60.0  # radians per second

	kTurningEncoderPositionPIDMinInput = 0  # radian
	kTurningEncoderPositionPIDMaxInput = kTurningEncoderPositionFactor  # radian

	kDrivingP = 0.04
	kDrivingI = 0
	kDrivingD = 0
	kDrivingFF = 1 / kDriveWheelFreeSpeedRps
	kDrivingMinOutput = -1
	kDrivingMaxOutput = 1

	kTurningP = 1
	kTurningI = 0
	kTurningD = 0
	kTurningFF = 0
	kTurningMinOutput = -1
	kTurningMaxOutput = 1

	kDrivingMotorIdleMode = CANSparkMax.IdleMode.kBrake
	kTurningMotorIdleMode = CANSparkMax.IdleMode.kBrake

	kDrivingMotorCurrentLimit = 50  # amp
	kTurningMotorCurrentLimit = 20  # amp


class OIConstants:
	kDriverControllerPort = 0
	kDriveDeadband = 0.05


class AutoConstants:
	# Speed controls in autonomous so the robot doesn't kill itself it uncontrolled testing
	kMaxSpeedMetersPerSecond = 3
	kMaxAccelerationMetersPerSecondSquared = 3
	kMaxAngularSpeedRadiansPerSecond = math.pi
	kMaxAngularSpeedRadiansPerSecondSquared = math.pi ^ 2

	kPXController = 1
	kPYController = 1
	kPThetaController = 1

	# Constraint for the motion profiled robot angle controller
	kThetaControllerConstraints = TrapezoidProfileRadians.Constraints(
		kMaxAngularSpeedRadiansPerSecond, kMaxAngularSpeedRadiansPerSecondSquared
	)


class ArmConstants:
	kSensorCountPerRevolution = 2048
	kDefaultMaxFowardRotation = 250 # Outward
	kMaxReverseRotation = 0; # Inward, starts fully inward so it starts in pos 0
	kDefaultMaxFowardRotationCount = kDefaultMaxFowardRotation * kSensorCountPerRevolution;
	"""Maximum motor rotation. May change dependant on design"""
	kReverseRotationCount = kMaxReverseRotation * kSensorCountPerRevolution;
	kArmFalconID = 4;
	"""The Falcon ID which belongs to the Arm. Depends on electrical setup (I think... idk I'm not in electrical)"""
	kLimitSwitchPort = 2;

	kP = 0.06277;
	"""PID variable: P stands for Proportional"""
	kI = 0;
	"""PID variable: I stands for Integral"""
	kD = 0;
	"""PID variable: D stands for Derivative"""
	kF = 0.049286;
	"""PID variable: The F component is a (experimentally determined) value that is added to the output"""
	kIZone = 0;

	kPeakOutput = 0.5;
	kStallCurrent = 20;
	"""(unsure) The motor current the arm will stall at (won't move)"""


class NetworkTableConstants:
	DEBUG = True;
	kNetworkTableInstance = NetworkTablesInstance.getDefault()
	kElevatorTable = kNetworkTableInstance.getTable("Elevator")
	kArmTable = kNetworkTableInstance.getTable("Arm")
	kDriveTable = kNetworkTableInstance.getTable("Drive")
	kPneumaticTable = kNetworkTableInstance.getTable("Pneumatic")


class PneumaticConstants:
	kRevPneumaticPort = 2;
	kClawFwdPort = 0;
	kClawRevPort = 1;
	kWristFwdPort = 2;
	kWristRevPort = 3;
	kClawMinPressure = 80;
	kClawMaxPressure = 90;
	kAnalogSensorPort = 0;


class PistonState(Enum):
	OPEN = "OPEN"
	CLOSED = "CLOSED"
	OFF = "OFF"


"""
Can IDs:
	0: PDP
	1:
	2: Rev PH
	3: Arm Falcon 500
	4: Elevator Falcon 500
	5: Front Right Swerve Drive Neo v1.1
	6: Front Left Swerve Drive Neo v1.1
	7: Back Right Swerve Drive Neo v1.1
	8: Back Left Swerve Drive Neo v1.1
	9: Front Right Swerve Steering Neo 550
	10: Front Left Swerve Steering Neo 550
	11: Back Right Swerve Steering Neo 550
	12: Back Left Swerve Steering Neo 550

DIO Ports:
	0: Elevator Bottom
	1: Arm Bottom

Controllers:
	PSP: 0: Driver:
		Axis:
			1: LJX:Swerve Left/Right
			2: LJY:Swerve Forward/Backward
			3: RJX:Swerve Rotate
			4: RJY:
			5: X-Hat:
			6: Y-Hat:
		Buttons:
			1: X: Zero NavX
			2: A: Reset Encoders
			3: B: Hold Position(X Pattern)
			4: Y:
			5: RB:
			6: LB:
			7: RT:
			8: LT:
			9: Back:
			10: Start: 
			11: LJ Click:
			12: RJ Click:

Left Flight Stick: 1: Operator
	Axis:
		1: X: 
		2: Y: Elevator Up/Down
		3: Z(Twist): 
		4: Throttle:
		5: X-Hat:
		6: Y-Hat:
	Buttons:
		1: Trigger: Log Robot Data
		2: Thumb Button:
		3: Back Left: 
		4: Back Right:
		5: Front Left:
		6: Front Right:
		7: Button 7:
		8: Button 8:
		9: Button 9:
		10: Button 10:
		11: Button 11:
		12: Button 12:

Right Flight Stick: 2: Operator
	Axis:
		1: X: 
		2: Y: Arm In/Out
		3: Z(Twist): 
		4: Throttle:
		5: X-Hat:
		6: Y-Hat:
	Buttons:
		1: Trigger: Claw Toggle
		2: Thumb Button: Toggle Compressor
		3: Back Left:
		4: Back Right: 
		5: Front Left: Claw Pneumatics Off
		6: Front Right:
		7: Button 7:
		8: Button 8:
		9: Button 9:
		10: Button 10:
		11: Button 11:
		12: Button 12:
"""