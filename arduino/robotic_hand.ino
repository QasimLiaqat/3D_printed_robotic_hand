#include <Servo.h>

// --------------------------------------------------
// 7 Servo Robotic Hand + Arm
// --------------------------------------------------

Servo finger1;
Servo finger2;
Servo finger3;
Servo finger4;
Servo finger5;

Servo armRotation;
Servo armLeftRight;

// Change these pins according to your wiring
const int FINGER1_PIN = 3;
const int FINGER2_PIN = 5;
const int FINGER3_PIN = 6;
const int FINGER4_PIN = 9;
const int FINGER5_PIN = 10;

const int ROTATION_PIN = 11;
const int LEFT_RIGHT_PIN = 12;

// Servo positions
int finger1Angle = 90;
int finger2Angle = 90;
int finger3Angle = 90;
int finger4Angle = 90;
int finger5Angle = 90;

int rotationAngle = 90;
int leftRightAngle = 90;

void setup() {

  Serial.begin(115200);

  finger1.attach(FINGER1_PIN);
  finger2.attach(FINGER2_PIN);
  finger3.attach(FINGER3_PIN);
  finger4.attach(FINGER4_PIN);
  finger5.attach(FINGER5_PIN);

  armRotation.attach(ROTATION_PIN);
  armLeftRight.attach(LEFT_RIGHT_PIN);

  // Initial position
  finger1.write(90);
  finger2.write(90);
  finger3.write(90);
  finger4.write(90);
  finger5.write(90);

  armRotation.write(90);
  armLeftRight.write(90);

  Serial.println("Robotic hand ready");
}

void loop() {

  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');

    int values[7];

    int index = 0;
    int start = 0;

    for (int i = 0; i <= data.length(); i++) {

      if (i == data.length() || data.charAt(i) == ',') {

        if (index < 7) {
          values[index] = data.substring(start, i).toInt();
          index++;
        }

        start = i + 1;
      }
    }

    if (index == 7) {

      finger1Angle = constrain(values[0], 0, 180);
      finger2Angle = constrain(values[1], 0, 180);
      finger3Angle = constrain(values[2], 0, 180);
      finger4Angle = constrain(values[3], 0, 180);
      finger5Angle = constrain(values[4], 0, 180);

      rotationAngle = constrain(values[5], 0, 180);
      leftRightAngle = constrain(values[6], 0, 180);

      finger1.write(finger1Angle);
      finger2.write(finger2Angle);
      finger3.write(finger3Angle);
      finger4.write(finger4Angle);
      finger5.write(finger5Angle);

      armRotation.write(rotationAngle);
      armLeftRight.write(leftRightAngle);
    }
  }
}