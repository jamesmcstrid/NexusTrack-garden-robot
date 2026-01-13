#include "config.h"
#include <Servo.h>

/**
 * NexusTrack Core Firmware - Phase 0 (RC-Car)
 * Version: 1.0 (2026-01-13)
 */

Servo steeringServo;

void setup() {
  // Starta seriell kommunikation för OnePlus 8T/Felsökning
  Serial.begin(115200);
  while (!Serial) { ; } // Vänta på anslutning
  
  Serial.println("--- NexusTrack System Init ---");

  // Konfigurera Motorer (L298N)
  pinMode(PIN_MOTOR_L_ENA, OUTPUT);
  pinMode(PIN_MOTOR_L_IN1, OUTPUT);
  pinMode(PIN_MOTOR_L_IN2, OUTPUT);
  pinMode(PIN_MOTOR_R_IN3, OUTPUT);
  pinMode(PIN_MOTOR_R_IN4, OUTPUT);
  pinMode(PIN_MOTOR_R_ENB, OUTPUT);

  // Konfigurera Servo
  steeringServo.attach(PIN_SERVO_STEERING);
  steeringServo.write(90); // Centrera styrning

  // Konfigurera alla Ultraljudssensorer
  setupSensor(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  setupSensor(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  setupSensor(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  setupSensor(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  setupSensor(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);

  Serial.println("System Ready. Monitoring 360 Coverage...");
}

void loop() {
  // 1. Läs av alla sensorer
  long distFC = getDistance(PIN_SENSOR_FC_TRIG, PIN_SENSOR_FC_ECHO);
  long distFL = getDistance(PIN_SENSOR_FL_TRIG, PIN_SENSOR_FL_ECHO);
  long distFR = getDistance(PIN_SENSOR_FR_TRIG, PIN_SENSOR_FR_ECHO);
  long distBL = getDistance(PIN_SENSOR_BL_TRIG, PIN_SENSOR_BL_ECHO);
  long distBR = getDistance(PIN_SENSOR_BR_TRIG, PIN_SENSOR_BR_ECHO);

  // 2. Skicka data till OnePlus 8T (JSON-format för framtida MQTT)
  Serial.print("{\"FC\":"); Serial.print(distFC);
  Serial.print(",\"FL\":"); Serial.print(distFL);
  Serial.print(",\"FR\":"); Serial.print(distFR);
  Serial.print(",\"BL\":"); Serial.print(distBL);
  Serial.print(",\"BR\":"); Serial.print(distBR);
  Serial.println("}");

  // 3. Säkerhetsstopp: Om något är närmare än SAFE_DISTANCE_CM
  if (distFC < SAFE_DISTANCE_CM && distFC > 0) {
    stopMotors();
    Serial.println("! SAFETY STOP: Obstacle Ahead !");
  }

  delay(100); // Kort paus för stabilitet
}

// --- HJÄLPFUNKTIONER ---

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
  
  long duration = pulseIn(echo, HIGH, 30000); // Timeout efter 30ms
  long distance = duration * 0.034 / 2;
  
  if (distance == 0) return MAX_DISTANCE_CM; // Inget eko = fri väg
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
