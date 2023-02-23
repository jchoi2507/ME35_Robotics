#include <Servo.h>

Servo servo1;
const int servoPin = 3; // Digital I/O pin # on Arduino Uno

const int maxAge = 80; // Maximum age possible reference (increase for less servo actuation,
                       //                                 decrease for more servo actuation)
const int maxAngle = 180; // Maximum angle rotation of servo

String predictedAge_str; // Serial input from Python script
int predictedAge; // Integer conversion of serial input

boolean state = true; // Condition to keep inputting serial data or not

// Determines how much to rotate servo by (in degrees)
int actuateServoBy(int age) {
  float factor = float(age)/float(maxAge);
  //Serial.println(factor);

  return (factor * maxAngle);
}

// Setup function
void setup() {
  Serial.begin(9600); // 9600 baudrate instead of 115200 used to slow down serial input
  servo1.attach(servoPin);
  servo1.write(0);
}

// Main looping function
void loop() {
   while (Serial.available())
    {
        while (state) {
          predictedAge_str = Serial.readStringUntil('\n');
          //Serial.println(predictedAge_str);

          if (predictedAge_str.length() == 2) {
            Serial.println("TEST");
            predictedAge = predictedAge_str.toInt();
            state = false;
          }
      }
        int angle = actuateServoBy(predictedAge);
        Serial.println(angle);
        servo1.write(angle);
        
        state = true;
        delay(1000);
    }
}
