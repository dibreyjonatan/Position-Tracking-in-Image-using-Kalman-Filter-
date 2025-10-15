import serial
from simple_pid import PID
port=""
baud_rate=0
inputValueYaw=0
movementYawAngle=0
####defining the angle parameters
MAX_YAW = 15    # Degrees / s 

pidYaw = None
P_YAW = 0.07 #orgineel 0.01 
#optimum at 0.07
I_YAW = 0
D_YAW = 0
###connexions
ser=None
#### paramètre du filtre 
a=[0.88176521]
b=[0.0591174, 0.0591174]
prev_output=0
prev_yawangle=0
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
    global ser,a,b,prev_output,prev_yawangle,movementYawAngle
    output=a[0]*prev_output+b[0]*value + b[1]*prev_yawangle
    prev_yawangle=value
    prev_output=output
    movementYawAngle=output
    #print(value,output) 
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