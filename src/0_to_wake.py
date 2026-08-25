#include <Servo.h>

Servo canopyServo;  // Create servo object to control the release

const int servoPin = 9;   // Pin connected to the servo signal wire
const int delayTime = 5000; // Time in milliseconds before release (5 seconds)

void setup() {
  canopyServo.attach(servoPin);
  canopyServo.write(0);   // Start at locked position (0 degrees)
  delay(1000);            // Wait for system to stabilize
}

void loop() {
  // Wait for the rocket to reach altitude or time delay
  delay(delayTime); 
  
  // Rotate canister lid to release the canopy
  canopyServo.write(90);  // Rotate to unlocked position (90 degrees)
  
  // Stop the program from repeating
  while(true); 
}
