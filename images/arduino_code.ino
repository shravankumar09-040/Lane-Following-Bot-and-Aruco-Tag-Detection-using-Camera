int IN1 = 8;    // Motor A direction pin 1
int IN2 = 7;    // Motor A direction pin 2
int IN3 = 10;    // Motor B direction pin 1
int IN4 = 11;    // Motor B direction pin 2
int ENA = 6;    // PWM pin for Motor A enable
int ENB = 9;    // PWM pin for Motor B enable


int speedValue = 130; // Motor speed (0–255)


void setup() {
 Serial.begin(9600);


 pinMode(IN1, OUTPUT);
 pinMode(IN2, OUTPUT);
 pinMode(IN3, OUTPUT);
 pinMode(IN4, OUTPUT);
 pinMode(ENA, OUTPUT);
 pinMode(ENB, OUTPUT);


 Serial.println("L298D Motor Control Ready");
}


void loop() {
 if (Serial.available() > 0) {
   char command = Serial.read();


   switch (command) {
     case 'F':
       moveForward();
       break;
     case 'B':
       moveBackward();
       break;
     case 'L':
       turnLeft();
       break;
     case 'R':
       turnRight();
       break;
     case 'S':
       stopMotors();
       break;
     default:
       Serial.println("Unknown command");
       break;
   }
 }
}


// ---------- Motor Control Functions ----------
void moveForward() {
 digitalWrite(IN1, HIGH);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, HIGH);
 digitalWrite(IN4, LOW);
 analogWrite(ENA, speedValue);
 analogWrite(ENB, speedValue);
 Serial.println("Moving Forward");
}


void moveBackward() {
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
 analogWrite(ENA, speedValue);
 analogWrite(ENB, speedValue);
 Serial.println("Moving Backward");
}


void turnLeft() {
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, HIGH);
 digitalWrite(IN3, HIGH);
 digitalWrite(IN4, LOW);
 analogWrite(ENA, speedValue);
 analogWrite(ENB, speedValue);
 Serial.println("Turning Left");
}


void turnRight() {
 digitalWrite(IN1, HIGH);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, HIGH);
 analogWrite(ENA, speedValue);
 analogWrite(ENB, speedValue);
 Serial.println("Turning Right");
}


void stopMotors() {
 digitalWrite(IN1, LOW);
 digitalWrite(IN2, LOW);
 digitalWrite(IN3, LOW);
 digitalWrite(IN4, LOW);
 analogWrite(ENA, 0);
 analogWrite(ENB, 0);
 Serial.println("Motors Stopped");
}

