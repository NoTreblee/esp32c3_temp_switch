## 📌 Project Overview

A lightweight MicroPython application for ESP32-C3 that reads temperature from a DHT11 sensor and controls a binary entity in Home Assistant based on configurable thresholds.

## 💡 Features
- Real-time temperature monitoring (1s interval)
- Automatic switch control via Home Assistant API
- Configurable thresholds (currently hardcoded, but planned to move to config)
- Minimal dependencies — runs on stock MicroPython

## 🧰 Hardware Requirements
- Espressif ESP32-C3 (tested)
- DHT11 temperature/humidity sensor
- WiFi connection to Home Assistant instance

## ⚙️ Setup
1. Clone or download the repository.
2. Edit `config.py` with your WiFi and HA credentials.
3. Flash MicroPython firmware to ESP32-C3.
4. Upload files using `ampy` or Thonny.
5. Run `main.py`.

## 📄 Configuration
Edit `config.py` to set:
- WiFi SSID & password
- Home Assistant URL and token
- Entity ID to control (e.g., `switch.heater`)
