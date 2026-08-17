# 3D Printed Robotic Hand Controlled by Human Hand

A real-time robotic hand and arm control system that follows human hand movements using a camera, Python computer vision, Arduino and 7 servo motors.

## Project Overview

This project uses a camera to detect human hand movements.

A Python computer vision program processes the camera feed and extracts hand landmarks. The detected movements are converted into servo motor commands and transmitted to an Arduino through serial communication.

The Arduino receives the commands and controls 7 servo motors.

## System Architecture

Camera
↓
Python
↓
OpenCV + MediaPipe
↓
Hand Landmark Detection
↓
Servo Angle Calculation
↓
Serial Communication
↓
Arduino
↓
7 Servo Motors
↓
3D Printed Robotic Hand & Arm

## Hardware

- Arduino
- 7 Servo Motors
- 3D Printed Robotic Hand
- Robotic Arm
- USB Camera
- Computer/Laptop

## Software

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino IDE
- Arduino C/C++

## Servo Configuration

| Servo | Function |
|------|----------|
| Servo 1 | Finger 1 |
| Servo 2 | Finger 2 |
| Servo 3 | Finger 3 |
| Servo 4 | Finger 4 |
| Servo 5 | Finger 5 |
| Servo 6 | Arm Rotation |
| Servo 7 | Arm Left/Right |

## Installation

Install Python dependencies:

```bash
pip install -r python/requirements.txt
