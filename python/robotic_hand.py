import cv2
import mediapipe as mp
import serial
import time
import math

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

SERIAL_PORT = "COM3"       # Change this to your Arduino port
BAUD_RATE = 115200

CAMERA_INDEX = 0

# Servo limits
MIN_SERVO = 20
MAX_SERVO = 160

# --------------------------------------------------
# SERIAL CONNECTION
# --------------------------------------------------

try:
    arduino = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1
    )

    time.sleep(2)

    print("Arduino connected.")

except Exception as e:
    print("Could not connect to Arduino.")
    print(e)
    arduino = None


# --------------------------------------------------
# MEDIAPIPE
# --------------------------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def distance(point1, point2):

    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )


def map_value(value, in_min, in_max, out_min, out_max):

    value = max(in_min, min(value, in_max))

    return int(
        (value - in_min) *
        (out_max - out_min) /
        (in_max - in_min)
        + out_min
    )


def finger_angle(hand_landmarks, tip_id, pip_id):

    tip = hand_landmarks.landmark[tip_id]
    pip = hand_landmarks.landmark[pip_id]

    # Distance from wrist to fingertip
    wrist = hand_landmarks.landmark[0]

    tip_distance = distance(wrist, tip)
    pip_distance = distance(wrist, pip)

    # Finger extended
    if tip_distance > pip_distance:
        return 20

    # Finger folded
    return 160


# --------------------------------------------------
# CAMERA
# --------------------------------------------------

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Could not open camera.")
    exit()


while True:

    success, frame = cap.read()

    if not success:
        print("Camera frame unavailable.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    # Default servo positions
    servo1 = 90
    servo2 = 90
    servo3 = 90
    servo4 = 90
    servo5 = 90

    rotation = 90
    left_right = 90


    # --------------------------------------------------
    # HAND DETECTED
    # --------------------------------------------------

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Draw hand skeleton
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )


        # --------------------------------------------------
        # FINGERS
        # --------------------------------------------------

        # Thumb
        thumb = hand.landmark[4]
        thumb_ip = hand.landmark[3]

        if distance(thumb, hand.landmark[0]) > \
           distance(thumb_ip, hand.landmark[0]):

            servo1 = 20

        else:

            servo1 = 160


        # Index
        servo2 = finger_angle(
            hand,
            8,
            6
        )

        # Middle
        servo3 = finger_angle(
            hand,
            12,
            10
        )

        # Ring
        servo4 = finger_angle(
            hand,
            16,
            14
        )

        # Little
        servo5 = finger_angle(
            hand,
            20,
            18
        )


        # --------------------------------------------------
        # ARM MOVEMENT
        # --------------------------------------------------

        wrist = hand.landmark[0]

        # X position controls left/right
        left_right = map_value(
            wrist.x,
            0.1,
            0.9,
            MIN_SERVO,
            MAX_SERVO
        )

        # Y position controls rotation
        rotation = map_value(
            wrist.y,
            0.1,
            0.9,
            MAX_SERVO,
            MIN_SERVO
        )


        # --------------------------------------------------
        # LIMIT VALUES
        # --------------------------------------------------

        servo_values = [

            max(MIN_SERVO, min(servo1, MAX_SERVO)),
            max(MIN_SERVO, min(servo2, MAX_SERVO)),
            max(MIN_SERVO, min(servo3, MAX_SERVO)),
            max(MIN_SERVO, min(servo4, MAX_SERVO)),
            max(MIN_SERVO, min(servo5, MAX_SERVO)),

            max(MIN_SERVO, min(rotation, MAX_SERVO)),
            max(MIN_SERVO, min(left_right, MAX_SERVO))
        ]


        # --------------------------------------------------
        # SEND TO ARDUINO
        # --------------------------------------------------

        if arduino:

            message = ",".join(
                str(value)
                for value in servo_values
            )

            arduino.write(
                (message + "\n").encode()
            )


        # Display values
        cv2.putText(
            frame,
            f"Servos: {servo_values}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )


    # --------------------------------------------------
    # DISPLAY
    # --------------------------------------------------

    cv2.imshow(
        "3D Robotic Hand Control",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()

hands.close()

if arduino:
    arduino.close()

print("Program stopped.")