import serial
from simple_pid import PID
port=""
baud_rate=0
inputValueYaw=0
movementYawAngle=0
####defining the angle parameters
MAX_YAW = 15    # Degrees / s 

pidYaw = None
P_YAW = 0.04 #orgineel 0.01 
#optimum at P=0.04 and I=0.001
I_YAW = 0.001
D_YAW = 0
###connexions
ser=None
def configure_PID():
    global pidRoll,pidYaw
    #Creates a new PID object depending on whether or not the PID or P is used 
    print("Configuring control")

    pidYaw = PID(P_YAW, I_YAW, D_YAW, setpoint=0)       # I = 0.001
    pidYaw.output_limits = (-MAX_YAW, MAX_YAW)          # PID Range 
    print("Configuring PID")

def connexion(p,b):
    global port,baud_rate,ser
    port=p
    baud_rate=b
    ser=serial.Serial(port,baud_rate)
    print("successful connexion")
def send_command(value):
    global ser
    print(value) 
    #ser=serial.Serial(port,baud_rate)
    
    ser.write((f'{value}\n').encode() )
def setXdelta(XDelta):
    global inputValueYaw
    inputValueYaw = XDelta 

def getMovementYawAngle():
    return movementYawAngle   
def control_servo():
    global movementYawAngle, movementRollAngle,pidYaw
    if inputValueYaw == 0:
        send_command(0)
    else:
         
        movementYawAngle = (pidYaw(inputValueYaw) * -1)
        send_command(movementYawAngle) 
        #Uncomment the previous ligne when you are done with the filter design