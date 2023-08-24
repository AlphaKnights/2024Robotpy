# WPI
from wpilib import DigitalInput
# WPI Math
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
from Constants import ArmConstants

class ArmSubsystem(SubsystemBase):
    ArmFalcon = TalonSRX(ArmConstants.kArmFalconID)
    FalconConfig = TalonSRXConfiguration()
    ArmPID = PIDController(ArmConstants.kP, ArmConstants.kI, ArmConstants.kD)
    ReverseLimiter = DigitalInput(ArmConstants.kLimitSwitchPort)

    m_maxArmPosition = ArmConstants.kDefaultMaxFowardRotationCount