from ctre import TalonFX
from ctre import TalonFXConfiguration
from ctre import ControlMode
from ctre import NeutralMode
from wpimath.controller import PIDController
from wpilib import DigitalInput
from Constants import ElevatorConstants 
from commands2 import SubsystemBase

# I put SubsystemBase because its from the docs, and like our java code alr
class ElevatorSubystem(SubsystemBase):

	def __init__(self):
		self.elevatorFalcon = TalonFX(ElevatorConstants.kElevatorFalconID)
		self.elevatorConfig = TalonFXConfiguration()
		self.reverseLimit = DigitalInput(ElevatorConstants.kReverseLimitSwitchPort)
		self.forwardLimit = DigitalInput(ElevatorConstants.kForwardLimitSwitchPort)
		self.elevatorPID = PIDController(ElevatorConstants.kP, ElevatorConstants.kI, ElevatorConstants.kD)
		self.m_maxElevatorVerticalPosition = ElevatorConstants.kDefaultMaxFowardVerticalRotation*ElevatorConstants.kSensorCountPerRevolution
		self.elevatorConfig.forwardSoftLimitEnable = False
		self.elevatorConfig.reverseSoftLimitEnable = False
		self.elevatorConfig.forwardSoftLimitThreshold = self.m_maxElevatorVerticalPosition
		self.elevatorConfig.reverseSoftLimitThreshold = ElevatorConstants.kMaxReverseVerticalRotationCount
		self.elevatorFalcon.configAllSettings(self.elevatorConfig)
		self.elevatorFalcon.setNeutralMode(NeutralMode.Brake)
		self.elevatorFalcon.setSelectedSensorPosition(ElevatorConstants.kMaxReverseVerticalRotationCount)
	
	
	def setPower(self, p_power):
		if(self.reverseLimit.get()):
			if(p_power < 0):
				self.elevatorFalcon.set(ControlMode.PercentOutput, 0)
			else:
				self.elevatorFalcon.set(ControlMode.PercentOutput, p_power)
			self.elevatorFalcon.setSelectedSensorPosition(ElevatorConstants.kMaxReverseVerticalRotationCount)
		elif(not self.forwardLimit.get()):
			if(p_power > 0):
				self.elevatorFalcon.set(ControlMode.PercentOutput, 0)
			else:
				self.elevatorFalcon.set(ControlMode.PercentOutput, p_power)
		else:
			self.elevatorFalcon.set(ControlMode.PercentOutput, p_power)


	def goToPosition(self):
		print(self.elevatorPID.calculate(self.elevatorFalcon.getSelectedSensorPosition()))
	
	
	def setToPosition(self):
		self.elevatorPID.setP(float(ElevatorConstants.kP))
		self.elevatorPID.setI(float(ElevatorConstants.kI))
		self.elevatorPID.setD(float(ElevatorConstants.kD))


	def homeElevatorBottom(self):
		if(self.reverseLimit.get()):
			return True 
		else:
			self.setPower(0)
			return False
	
	
	def homeElevatorTop(self):
		if(self.forwardLimit.get()):
			self.elevatorFalcon.configForwardSoftLimitThreshold(self.elevatorFalcon.getSelectedSensorPosition())
			self.setPower(0)
			return True
		else:
			self.setPower(.5)
			return False
	
	
	def homeElevator(self):
		if(self.homeElevatorBottom()):
			return self.homeElevatorTop()
		else:
			return self.homeElevatorBottom()
	
	
	def getPosition(self):
		return self.elevatorFalcon.getSelectedSensorPosition()