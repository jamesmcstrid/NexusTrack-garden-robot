#ifndef NEXUS_CONFIG_H
#define NEXUS_CONFIG_H

/**
 * NexusTrack - Prototyp Fas 0 (RC-bil)
 * Pin-konfiguration för Elegoo Mega 2560
 */

// --- OFFICIELLA NAMN FÖR MQTT & NODE-RED ---
#define J_FC   "d_fc"
#define J_FL   "d_fl"
#define J_FR   "d_fr"
#define J_BL   "d_bl"
#define J_BR   "d_br"
#define J_BATT "batt"
#define J_STAT "status"

// --- STYRNING ---
#define PIN_SERVO_STEERING 9

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

// --- INSTÄLLNINGAR ---
#define MAX_DISTANCE_CM 200    
#define SAFE_DISTANCE_CM 20   
#define DEFAULT_SPEED 150     

#endif // NEXUS_CONFIG_H