#include "config.h"
#include <Servo.h>

Servo steeringServo;

// Globala variabler för sensorvärden
long distFC, distFL, distFR, distBL, distBR;
String currentStatus = "IDLE";

void setup() {
  Serial.begin(115200);
  
  // Motor-konfiguration
  pinMode(PIN_MOTOR_L_ENA, OUTPUT);
  pinMode(PIN_MOTOR_L_IN1, OUTPUT);
  pinMode(PIN_MOTOR_L_IN2, OUTPUT);
  pinMode(PIN_MOTOR_R_IN3, OUTPUT);
  pinMode(PIN_MOTOR_R_IN4, OUTPUT);
  pinMode(PIN_MOTOR_R_ENB, OUTPUT);

  // Servo-konfiguration
  steeringServo.attach(PIN_SERVO_STEERING);
  steeringServo.write(SERVO_CENTER); 

  // Sensor-konfiguration
  setupSensor(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  setupSensor(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  setupSensor(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  setupSensor(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  setupSensor(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);

  currentStatus = "BOOTING";
  sendTelemetry();
  delay(2000);
}

void loop() {
  // 1. Läs av omgivningen
  readAllSensors();

  // 2. Autonom logik (Beslutsfattning)
  if (distFC < SAFE_DISTANCE_CM && distFC > 0) {
    // HINDER UPPTÄCKT!
    currentStatus = "OBSTACLE_DETECTED";
    sendTelemetry();
    
    executeEvasion(); // Kör undanmanöver
  } else {
    // FRI VÄG!
    currentStatus = "DRIVING_FORWARD";
    steeringServo.write(SERVO_CENTER);
    driveForward(DEFAULT_SPEED);
  }

  // 3. Uppdatera Dashboard
  sendTelemetry();
  delay(50); 
}

// --- MANÖVER-LOGIK ---

void executeEvasion() {
  stopMotors();
  delay(500);

  // Bestäm svängriktning baserat på sidosensorer
  if (distFL > distFR) {
    steeringServo.write(SERVO_LEFT);
    currentStatus = "EVADING_LEFT";
  } else {
    steeringServo.write(SERVO_RIGHT);
    currentStatus = "EVADING_RIGHT";
  }
  
  sendTelemetry();
  
  // Backa ut ur situationen
  driveBackward(TURN_SPEED);
  delay(BACKUP_TIME);
  
  stopMotors();
  steeringServo.write(SERVO_CENTER);
  delay(200);
}

// --- MOTORSTYRNING ---

void driveForward(int spd) {
  digitalWrite(PIN_MOTOR_L_IN1, HIGH);
  digitalWrite(PIN_MOTOR_L_IN2, LOW);
  digitalWrite(PIN_MOTOR_R_IN3, HIGH);
  digitalWrite(PIN_MOTOR_R_IN4, LOW);
  analogWrite(PIN_MOTOR_L_ENA, spd);
  analogWrite(PIN_MOTOR_R_ENB, spd);
}

void driveBackward(int spd) {
  digitalWrite(PIN_MOTOR_L_IN1, LOW);
  digitalWrite(PIN_MOTOR_L_IN2, HIGH);
  digitalWrite(PIN_MOTOR_R_IN3, LOW);
  digitalWrite(PIN_MOTOR_R_IN4, HIGH);
  analogWrite(PIN_MOTOR_L_ENA, spd);
  analogWrite(PIN_MOTOR_R_ENB, spd);
}

void stopMotors() {
  analogWrite(PIN_MOTOR_L_ENA, 0);
  analogWrite(PIN_MOTOR_R_ENB, 0);
  digitalWrite(PIN_MOTOR_L_IN1, LOW);
  digitalWrite(PIN_MOTOR_L_IN2, LOW);
  digitalWrite(PIN_MOTOR_R_IN3, LOW);
  digitalWrite(PIN_MOTOR_R_IN4, LOW);
}

// --- SENSORER & TELEMETRI ---

void readAllSensors() {
  distFC = getDistance(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  distFL = getDistance(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  distFR = getDistance(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  distBL = getDistance(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  distBR = getDistance(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);
}

long getDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  long duration = pulseIn(echo, HIGH, 25000); // Timeout efter 25ms
  long distance = duration * 0.034 / 2;
  if (distance <= 0 || distance > MAX_DISTANCE_CM) return MAX_DISTANCE_CM;
  return distance;
}

void setupSensor(int trig, int echo) {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
}

void sendTelemetry() {
  Serial.print("{");
  Serial.print("\"" J_FC "\":"); Serial.print(distFC); Serial.print(",");
  Serial.print("\"" J_FL "\":"); Serial.print(distFL); Serial.print(",");
  Serial.print("\"" J_FR "\":"); Serial.print(distFR); Serial.print(",");
  Serial.print("\"" J_BL "\":"); Serial.print(distBL); Serial.print(",");
  Serial.print("\"" J_BR "\":"); Serial.print(distBR); Serial.print(",");
  Serial.print("\"" J_STAT "\":\""); Serial.print(currentStatus); Serial.print("\",");
  Serial.print("\"" J_BATT "\":100"); // Placeholder
  Serial.println("}");
}