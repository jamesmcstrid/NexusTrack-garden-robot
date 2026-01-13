#ifndef NEXUS_CONFIG_H
#define NEXUS_CONFIG_H

/**
 * NexusTrack - Prototyp Fas 0 (RC-bil)
 * Pin-konfiguration för Elegoo Mega 2560
 */

// --- MOTOR DRIVER (L298N) ---
// Hastighet (PWM) och riktning
#define PIN_MOTOR_L_ENA 2
#define PIN_MOTOR_L_IN1 3
#define PIN_MOTOR_L_IN2 4
#define PIN_MOTOR_R_IN3 5
#define PIN_MOTOR_R_IN4 6
#define PIN_MOTOR_R_ENB 7

// --- STYRNING (SERVO) ---
// Används för framaxelstyrning på RC-chassit
#define PIN_SERVO_STEERING 9

// --- ULTRALJUDSSENSORER (HC-SR04) ---
// Trig och Echo för 360-graders täckning
// FC = Front Center
#define PIN_SENSOR_FC_TRIG 22
#define PIN_SENSOR_FC_ECHO 23

// FL = Front Left (45 grader)
#define PIN_SENSOR_FL_TRIG 24
#define PIN_SENSOR_FL_ECHO 25

// FR = Front Right (45 grader)
#define PIN_SENSOR_FR_TRIG 26
#define PIN_SENSOR_FR_ECHO 27

// BL = Back Left (135 grader)
#define PIN_SENSOR_BL_TRIG 28
#define PIN_SENSOR_BL_ECHO 29

// BR = Back Right (135 grader)
#define PIN_SENSOR_BR_TRIG 30
#define PIN_SENSOR_BR_ECHO 31

// --- INSTÄLLNINGAR ---
#define MAX_DISTANCE_CM 200    // Max räckvidd för sensorerna
#define SAFE_DISTANCE_CM 20   // Avstånd för att stanna/väja
#define DEFAULT_SPEED 150     // Standardhastighet PWM (0-255)

#endif // NEXUS_CONFIG_H