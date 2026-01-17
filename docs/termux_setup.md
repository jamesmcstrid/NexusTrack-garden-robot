# 📱 Termux Setup Guide - OnePlus 8T

Denna guide beskriver hur du sätter upp Python-miljön på din OnePlus 8T för att fungera som robotens hjärna och kommunicera med Elegoo Mega 2560.

## 1. Grundläggande installation
Öppna Termux och kör följande kommandon för att uppdatera systemet och installera nödvändiga paket:
```bash
pkg update && pkg upgrade
pkg install python python-pip termux-api