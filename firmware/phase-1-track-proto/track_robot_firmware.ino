// Motor-pins för L298N
const int motorA1 = 9; const int motorA2 = 8; const int enA = 10;

void setup() {
  Serial.begin(9600); // Kommunikation med OnePlus 8T
  pinMode(motorA1, OUTPUT); pinMode(motorA2, OUTPUT); pinMode(enA, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'F') moveForward();
    else if (cmd == 'S') stopMotors();
  }
}

void moveForward() { digitalWrite(motorA1, HIGH); digitalWrite(motorA2, LOW); analogWrite(enA, 200); }
void stopMotors() { digitalWrite(motorA1, LOW); digitalWrite(motorA2, LOW); }