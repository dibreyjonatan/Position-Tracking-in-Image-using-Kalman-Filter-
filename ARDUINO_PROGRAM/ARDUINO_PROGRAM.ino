#include <Servo.h>

Servo myservo;  // create Servo object to control a servo

float val,yawangle ;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the Servo object
}

void loop() {
      if(Serial.available()){   
    val=Serial.readStringUntil('\n').toFloat(); // converts string to float value    
  yawangle= map(-val, -15, 15, 0, 180);     // scale it for use with the servo (value between 0 and 180)
  myservo.write(yawangle);                 // sets the servo position according to the scaled value
  delay(15);                           // waits for the servo to get there
}
}
