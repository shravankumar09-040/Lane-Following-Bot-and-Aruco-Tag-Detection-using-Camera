#!/usr/bin/env python3
import cv2
import numpy as np
import serial
import time
import threading

# ===============================
# GLOBAL VARIABLE (shared)
# ===============================
error = 999   # default = stop
lock = threading.Lock()

# ===============================
# CAMERA THREAD
# ===============================
def vision_thread():
    global error

    FRAME_WIDTH = 320
    FRAME_HEIGHT = 240

    lower_red1 = np.array([0, 110, 70])
    upper_red1 = np.array([8, 255, 255])
    lower_red2 = np.array([165, 110, 70])
    upper_red2 = np.array([180, 255, 255])

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        local_error = 999   # default = stop

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Optional: Remove noise
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest) > 500:

                # Draw contour
                cv2.drawContours(frame, [largest], -1, (0,255,0), 2)

                # Calculate centroid
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # Draw centroid
                    cv2.circle(frame, (cX, cY), 6, (255,0,0), -1)

                    # Draw center line
                    cv2.line(frame, (FRAME_WIDTH//2, 0),
                            (FRAME_WIDTH//2, FRAME_HEIGHT),
                            (255,255,0), 1)

                    # Error calculation (for debugging)
                    local_error = cX - (FRAME_WIDTH // 2)

                    # Display text
                    cv2.putText(frame, f"Centroid: ({cX},{cY})",
                                (10, 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0,255,255), 1)

                    cv2.putText(frame, f"Error: {local_error}",
                                (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0,255,255), 1)




        with lock:
            error = local_error

        cv2.imshow("Red Detection", frame)
        cv2.imshow("Mask", mask)

        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release AFTER loop ends
    cap.release()
    cv2.destroyAllWindows()

# ===============================
# MOTOR THREAD
# ===============================
def motor_thread():
    global error

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)

    threshold = 25
    last_command = None

    while True:
        with lock:
            current_error = error

        if current_error == 999:
            command = 'S'
        elif current_error > threshold:
            command = 'R'
        elif current_error < -threshold:
            command = 'L'
        else:
            command = 'F'

        if command != last_command:
            ser.write(command.encode())
            print("Sent:", command)
            last_command = command

        time.sleep(0.05)


# ===============================
# START THREADS
# ===============================
t1 = threading.Thread(target=vision_thread)
t2 = threading.Thread(target=motor_thread)

t1.start()
t2.start()

t1.join()
t2.join()

