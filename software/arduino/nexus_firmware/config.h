#ifndef NEXUS_CONFIG_H
#define NEXUS_CONFIG_H

/**
 * NexusTrack - Prototyp Fas 0 (RC-bil)
 * Pin-konfiguration för Elegoo Mega 2560
 */

// --- OFFICIELLA NAMN FÖR MQTT & NODE-RED ---
#define J_FC    "d_fc"    // Distance Front Center
#define J_FL    "d_fl"    // Distance Front Left
#define J_FR    "d_fr"    // Distance Front Right
#define J_BL    "d_bl"    // Distance Back Left
#define J_BR    "d_br"    // Distance Back Right
#define J_BATT  "batt"    // Arduino Battery (Volt/%)
#define J_STAT  "status"  // Robot Status message

// --- STYRNING (Servo) ---
#define PIN_SERVO_STEERING 9
#define SERVO_CENTER 90
#define SERVO_LEFT   60   // Justera dessa efter din bils mekanik
#define SERVO_RIGHT  120

// --- MOTOR PINS (L298N) ---
#define PIN_MOTOR_L_ENA 2
#define PIN_MOTOR_L_IN1 3
#define PIN_MOTOR_L_IN2 4
#define PIN_MOTOR_R_IN3 5
#define PIN_MOTOR_R_IN4 6
#define PIN_MOTOR_R_ENB 7

// --- ULTRALJUDSSENSORER (HC-SR04) ---
#define PIN_SENSOR_FC_TRIG 22
#define PIN_SENSOR_FC_ECHO 23
#define PIN_SENSOR_FL_TRIG 24
#define PIN_SENSOR_FL_ECHO 25
#define PIN_SENSOR_FR_TRIG 26
#define PIN_SENSOR_FR_ECHO 27
#define PIN_SENSOR_BL_TRIG 28
#define PIN_SENSOR_BL_ECHO 29
#define PIN_SENSOR_BR_TRIG 30
#define PIN_SENSOR_BR_ECHO 31

// --- INSTÄLLNINGAR FÖR LOGIK ---
#define MAX_DISTANCE_CM 200     // Ignonera allt över 2 meter
#define SAFE_DISTANCE_CM 35     // Avstånd för att reagera på hinder
#define DEFAULT_SPEED 160       // Marschfart (0-255)
#define TURN_SPEED 140          // Hastighet vid manövrering
#define BACKUP_TIME 1200        // Hur länge den backar (ms)

#endif