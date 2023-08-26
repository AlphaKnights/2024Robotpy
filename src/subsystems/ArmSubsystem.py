# WPI
from wpilib import DigitalInput
# WPI Math
import MathUtil # for things that I cannot find in wpi math but are supposed to be there
from wpimath.controller import PIDController
# WPI Command-based
from commands2 import SubsystemBase
# Motor Control
from ctre import ControlMode
from ctre import NeutralMode
from ctre import TalonSRX
from ctre import TalonSRXConfiguration
# Other
import networktables as nt
# Robot Files
from Constants import ArmConstants, NetworkTablesConstants

class ArmSubsystem(SubsystemBase):
	# If you are familiar with Java, this is (essentially) a constructor.
	def __init__(self):
		# Initializing Motor(s) and PID controls
		self.ArmFalcon = TalonSRX(ArmConstants.kArmFalconID)
		self.FalconConfig = TalonSRXConfiguration()
		self.ArmPID = PIDController(ArmConstants.kP, ArmConstants.kI, ArmConstants.kD)
		self.ReverseLimiter = DigitalInput(ArmConstants.kLimitSwitchPort)

		self.m_maxArmPosition = ArmConstants.kDefaultMaxFowardRotationCount
		# Get NT PID values
		self.armEntryP = NetworkTablesConstants.kArmTable.getEntry("P")
		self.armEntryI = NetworkTablesConstants.kArmTable.getEntry("I")
		self.armEntryD = NetworkTablesConstants.kArmTable.getEntry("D")
		# Setting other values (need to ask what these mean)
		self.armFwdLimitEntry = NetworkTablesConstants.kArmTable.getEntry("FwdLimit")
		self.armRvsLimitEntry = NetworkTablesConstants.kArmTable.getEntry("RvsLimit")
		self.armPositionEntry = NetworkTablesConstants.kArmTable.getEntry("Position")
		self.armPowerEntry = NetworkTablesConstants.kArmTable.getEntry("Power")
		self.ingoreArmFwdLimitEntry = NetworkTablesConstants.kArmTable.getEntry("IngoreFwdLimit")
		self.powerLimitEntry = NetworkTablesConstants.kArmTable.getEntry("PowerLimit")
		self.ignoreLimitEntry = NetworkTablesConstants.kArmTable.getEntry("IgnoreLimit")
		# Setting NT defualts using constants (mostly)
		self.armEntryP.setDefaultDouble(ArmConstants.kP)
		self.armEntryI.setDefaultDouble(ArmConstants.kI)
		self.armEntryD.setDefaultDouble(ArmConstants.kD)
		self.armFwdLimitEntry.setDefaultBoolean(False)
		self.armRvsLimitEntry.setDefaultBoolean(False)
		self.armPositionEntry.setDefaultDouble(ArmConstants.kReverseRotationCount)
		self.armPowerEntry.setDefaultDouble(0.0)
		self.ingoreArmFwdLimitEntry.setDefaultBoolean(False)
		self.powerLimitEntry.setDefaultDouble(ArmConstants.kStallCurrent)
		# Falcon Configuration
		self.FalconConfig.forwardSoftLimitEnable = False
		self.FalconConfig.reverseSoftLimitEnable = False
		self.FalconConfig.forwardSoftLimitThreshold = self.m_maxArmPosition
		self.FalconConfig.reverseSoftLimitThreshold = ArmConstants.kReverseRotationCount
		self.FalconConfig.slot0.kP = ArmConstants.kP
		self.FalconConfig.slot0.kI = ArmConstants.kI
		self.FalconConfig.slot0.kD = ArmConstants.kD
		self.FalconConfig.slot0.kF = ArmConstants.kF
		self.FalconConfig.slot0.integralZone = ArmConstants.kIZone
		self.FalconConfig.slot0.closedLoopPeakOutput = ArmConstants.kPeakOutput
		self.ArmFalcon.configAllSettings(self.FalconConfig)
		# Setting additional Falcon components
		self.ArmFalcon.setNeutralMode(NeutralMode.Brake)
		self.ArmFalcon.setSelectedSensorPosition(ArmConstants.kReverseRotationCount)
	

	def setPower(self, p_power, elvPos): # What the fuck is elvPos
		"""
		Set the power output for Falcon-controlled motors in the arm
		:param p_power: 
		:param elvPos: No fucking clue
		"""
		self.armRvsLimitEntry.setBoolean(self.ReverseLimiter.get())
		self.armFwdLimitEntry.setBoolean(self.ArmFalcon.getStatorCurrent()>ArmConstants.kStallCurrent)
		self.armPositionEntry.setDouble(self.ArmFalcon.getSelectedSensorPosition()/ArmConstants.kSensorCountPerRevolution)
		self.armPowerEntry.setDouble(self.ArmFalcon.getStatorCurrent())

		# If IgnoreLimit is enabled on the ArmTable (NetT), set 'ReverseSoftLimit' to True on the falcon, otherwise false
		self.ArmFalcon.configReverseSoftLimitEnable(True if self.ignoreLimitEntry.getBoolean(True) else False)

		if (self.ingoreArmFwdLimitEntry.getBoolean(True)):
			# With no parameters, .get() for the DigitalInput object will return on true or false, 
			# true if it returns with a number, false if not
			# (so this is if there is no limiter value)
			if (not self.ReverseLimiter.get()):
				self.ArmFalcon.setSelectedSensorPosition(ArmConstants.kReverseRotationCount)

				# Set the Falcom power output to p_power if is more than 0, otherwise set to 0
				self.ArmFalcon.set(ControlMode.PercentOutput, 0 if p_power > 0 else p_power)

		# Stator current = output current
		# If the robot will not Ignore the Arm's Forward Limit, 
		# Make sure the Falcon's output current is more than the Falkon's power limit
		# Still dont know what elvPos is though. Elevator position?
		elif (self.ArmFalcon.getStatorCurrent() > self.powerLimitEntry.getDouble(ArmConstants.kStallCurrent) and 
				elvPos > (80*2048)):
			
			# p_power < 0 is repetative, find solution
			self.ArmFalcon.set(ControlMode.PercentOutput, 0 if p_power < 0 else p_power)
			if (p_power < 0):
				self.m_maxArmPosition = self.ArmFalcon.getSelectedSensorPosition()

		elif (elvPos > (80*2048) and 
				self.ArmFalcon.getSelectedSensorPosition() < (8*2048)):
			
			self.ArmFalcon.set(ControlMode.PercentOutput, p_power)
		elif (elvPos > (120*2048)):
			self.ArmFalcon.set(ControlMode.PercentOutput, p_power)
		else:
			self.ArmFalcon.set(ControlMode.PercentOutput, 0)


	def goToPosition(self, p_position, elvPos):
		"""
		Move the arm to a new location
		:param p_position: Current motor sensor position
		:param elvPos: No fucking clue
		"""
		# Restores the sensor position to the desired position with minimal delay and overshoot by...
		new_power_output = self.ArmPID.calculate(self.ArmFalcon.getSelectedSensorPosition(), 
							p_position * ArmConstants.kF)
		# (making sure the power output isn't OOB so-to-speak)
		new_power_output = MathUtil.clamp(new_power_output,
											-ArmConstants.kPeakOutput,
											ArmConstants.kPeakOutput)
		# increasing/decreasing the power output of the motor
		self.setPower(new_power_output, elvPos)
	
	
	def getPosition(self):
		return self.ArmFalcon.getSelectedSensorPosition()
	

	def getArmFalcon(self):
		"Gets the Arm Falcon object, for debugging use only."
		
		return self.ArmFalcon


	def getLimitSwitch(self):
		"Gets the Arm limit switch object, for debugging use only."

		return self.ReverseLimiter


	def test():
		ArmPID = PIDController(ArmConstants.kP, ArmConstants.kI, ArmConstants.kD)
		ArmPID.calculate()