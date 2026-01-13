#include "config.h"
#include <Servo.h>

/**
 * NexusTrack Core Firmware - Phase 0 (RC-Car)
 * Version: 1.1 (Uppdaterad med officiell namngivning)
 */

Servo steeringServo;

// Globala variabler för att sendTelemetry ska kunna läsa dem
long distFC, distFL, distFR, distBL, distBR;

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; } 
  
  Serial.println("--- NexusTrack System Init ---");

  // Motor-pins konfigureras här (Se till att dessa finns i config.h)
  pinMode(PIN_MOTOR_L_ENA, OUTPUT);
  pinMode(PIN_MOTOR_L_IN1, OUTPUT);
  pinMode(PIN_MOTOR_L_IN2, OUTPUT);
  pinMode(PIN_MOTOR_R_IN3, OUTPUT);
  pinMode(PIN_MOTOR_R_IN4, OUTPUT);
  pinMode(PIN_MOTOR_R_ENB, OUTPUT);

  steeringServo.attach(PIN_SERVO_STEERING);
  steeringServo.write(90); 

  setupSensor(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  setupSensor(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  setupSensor(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  setupSensor(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  setupSensor(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);

  Serial.println("System Ready. Monitoring 360 Coverage...");
}

void loop() {
  // 1. Läs av alla sensorer (sparas i globala variabler)
  distFC = getDistance(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  distFL = getDistance(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  distFR = getDistance(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  distBL = getDistance(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  distBR = getDistance(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);

  // 2. Skicka data till OnePlus 8T med officiella nycklar
  sendTelemetry();

  // 3. Säkerhetsstopp
  if (distFC < SAFE_DISTANCE_CM && distFC > 0) {
    stopMotors();
    // Skicka även statusuppdatering till Node-RED
    Serial.print("{\""); Serial.print(J_STAT); Serial.println("\":\"SAFETY_STOP\"}");
  }

  delay(100); 
}

// --- HJÄLPFUNKTIONER ---

void sendTelemetry() {
  // Här använder vi namnen från config.h (J_FC, J_FL etc.)
  Serial.print("{");
  Serial.print("\"" J_FC "\":"); Serial.print(distFC); Serial.print(",");
  Serial.print("\"" J_FL "\":"); Serial.print(distFL); Serial.print(",");
  Serial.print("\"" J_FR "\":"); Serial.print(distFR); Serial.print(",");
  Serial.print("\"" J_BL "\":"); Serial.print(distBL); Serial.print(",");
  Serial.print("\"" J_BR "\":"); Serial.print(distBR); Serial.print(",");
  Serial.print("\"" J_BATT "\":"); Serial.print(calculateBattery());
  Serial.println("}");
}

int calculateBattery() {
  // Provisorisk funktion - returnerar 100% tills vi kopplat spänningsdelaren
  return 100; 
}

void setupSensor(int trig, int echo) {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
}

long getDistance(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  
  long duration = pulseIn(echo, HIGH, 30000); 
  long distance = duration * 0.034 / 2;
  
  if (distance <= 0 || distance > MAX_DISTANCE_CM) return MAX_DISTANCE_CM; 
  return distance;
}

void stopMotors() {
  digitalWrite(PIN_MOTOR_L_IN1, LOW);
  digitalWrite(PIN_MOTOR_L_IN2, LOW);
  digitalWrite(PIN_MOTOR_R_IN3, LOW);
  digitalWrite(PIN_MOTOR_R_IN4, LOW);
  analogWrite(PIN_MOTOR_L_ENA, 0);
  analogWrite(PIN_MOTOR_R_ENB, 0);
}
// --- MOTORSTYRNING: KÖR FRAMÅT ---
void driveForward(int speed) {
  // Vänster motor
  digitalWrite(PIN_MOTOR_L_IN1, HIGH);
  digitalWrite(PIN_MOTOR_L_IN2, LOW);
  analogWrite(PIN_MOTOR_L_ENA, speed);

  // Höger motor
  digitalWrite(PIN_MOTOR_R_IN3, HIGH);
  digitalWrite(PIN_MOTOR_R_IN4, LOW);
  analogWrite(PIN_MOTOR_R_ENB, speed);
}

// --- UPPDATERAD LOOP FÖR AUTONOMI ---
void loop() {
  // 1. Läs sensorer
  distFC = getDistance(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  // ... läs övriga sensorer ...

  // 2. Skicka data till Dashboard (LXC 104)
  sendTelemetry();

  // 3. Beslutsfattning (Logik)
  if (distFC < SAFE_DISTANCE_CM && distFC > 0) {
    stopMotors(); // Hinder! Stanna omedelbart.
    Serial.print("{\""); Serial.print(J_STAT); Serial.println("\":\"OBSTACLE_STOP\"}");
  } else {
    driveForward(DEFAULT_SPEED); // Fri väg! Kör framåt.
    Serial.print("{\""); Serial.print(J_STAT); Serial.println("\":\"DRIVING\"}");
  }

  delay(100); 
}