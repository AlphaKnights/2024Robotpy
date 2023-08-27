# WPI
from wpilib import PneumaticHub, PneumaticsModuleType, DoubleSolenoid
# WPI Command-based
from commands2 import SubsystemBase
# Robot Files
from Constants import PneumaticConstants, NetworkTableConstants, PistonState
# Other
import networktables as nt

class ArmSubsystem(SubsystemBase):

	def __init__(self):
		self.pneumaticHub = PneumaticHub(PneumaticConstants.kRevPneumaticPort)
		# Setting up potitioning for the claw
		self.clawPiston = DoubleSolenoid(PneumaticConstants.kRevPneumaticPort, 
									PneumaticsModuleType.REVPH,
									PneumaticConstants.kClawFwdPort,
									PneumaticConstants.kClawRevPort)
		# Setting up SmartDashboard for compressor and double solenoid statuses
		self.m_minPressure = PneumaticConstants.kClawMinPressure
		self.m_maxPressure = PneumaticConstants.kClawMaxPressure
		self.pressureEntry = NetworkTableConstants.kPneumaticTable.getEntry("Pressure")
		self.clawPositionEntry = NetworkTableConstants.kPneumaticTable.getEntry("ClawPosition")
		self.wristPositionEntry = NetworkTableConstants.kPneumaticTable.getEntry("WristPosition")
		self.minPressureEntry = NetworkTableConstants.kPneumaticTable.getEntry("MinPressure")
		self.maxPressureEntry = NetworkTableConstants.kPneumaticTable.getEntry("MaxPressure")
		# Setting NT defaults
		self.pressureEntry.setDefaultDouble(0.0)
		self.clawPositionEntry.setDefaultString(PistonState.OFF) # I DO NOT KNOW HOW ENUMS WORK
		self.wristPositionEntry.setDefaultString(PistonState.OFF) # I DO NOT KNOW HOW ENUMS WORK
		self.minPressureEntry.setDefaultDouble(self.m_minPressure)
		self.maxPressureEntry.setDefaultDouble(self.m_maxPressure)


	def periodic(self):
			"""This method will be called once per scheduler run"""
			self.pressureEntry.setDouble(self.pneumaticHub.getPressure(0));
			self.clawPositionEntry.setString(self.getClawState().toString());
			self.wristPositionEntry.setString(self.getWristState().toString());
	

	def setClawState(self, p_state):
		match p_state:
			case PistonState.OPEN:
				self.clawPiston.set(DoubleSolenoid.Value.kForward)
			case PistonState.CLOSED:
				self.clawPiston.set(DoubleSolenoid.Value.kReverse)
			case PistonState.OFF:
				self.clawPiston.set(DoubleSolenoid.Value.kOff)


	def getClawState(self):
		match self.clawPiston.get():
			case self.kForward:
				return PistonState.OPEN
			case self.kReverse:
				return PistonState.CLOSED
			case self.kOff:
				return PistonState.OFF
			case _: # Java "default" equivalent
				return PistonState.OFF
	

	def setWristState(self, p_state):
		match p_state:
			case PistonState.OPEN:
				self.wristPiston.set(DoubleSolenoid.Value.kForward)
			case PistonState.CLOSED:
				self.wristPiston.set(DoubleSolenoid.Value.kReverse)
			case PistonState.OFF:
				self.wristPiston.set(DoubleSolenoid.Value.kOff)


	def getWristState(self):
		match self.wristPiston.get():
			case self.kForward:
				return PistonState.OPEN
			case self.kReverse:
				return PistonState.CLOSED
			case self.kOff:
				return PistonState.OFF
			case _: # Java "default" equivalent
				return PistonState.OFF


	def setCompressorPressure(self, p_min, p_max):
		"""
		Sets the pressure for the compressor
		:param p_min: minimum pressure
		:param p_max: maximum pressure
		"""
		self.pneumaticHub.enableCompressorAnalog(p_min, p_max)


	def disableCompressor(self):
		"""Disables the compressor"""
		self.pneumaticHub.disableCompressor()


	def toggleCompressor(self):
		"""Toggles the compressor on or off"""
		if(self.pneumaticHub.getCompressor()):
			self.disableCompressor()
		else:
			self.setCompressorPressure(self.minPressureEntry.getDouble(self.m_minPressure), 
			      						self.maxPressureEntry.getDouble(self.m_maxPressure))


	def toggleCompressor(self, p_min, p_max):
		"""
		Toggles the compressor on or off
		:param p_min: minimum pressure
   		:param p_max: maximum pressure
		"""
		if(self.pneumaticHub.getCompressor()):
			self.disableCompressor()
		else:
			self.setCompressorPressure(p_min, p_max)