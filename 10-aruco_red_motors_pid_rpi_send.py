#!/usr/bin/env python3
import cv2
import numpy as np
import serial
import time
import threading
import cv2.aruco as aruco

import requests



RPI_IP = "172.21.7.4"  # Change this

def send_to_rpi(cmd):
    try:
        requests.get(f"http://{RPI_IP}:5000/cmd/{cmd}")
    except:
        print("RPi not reachable")


# ===============================
# GLOBAL VARIABLE (shared)
# ===============================
error = 999   # default = stop
lock = threading.Lock()

aruco_command = None
aruco_last_time = 0

# ===============================
# CAMERA THREAD
# ===============================
def vision_thread():
    global error, aruco_command, aruco_last_time
    

    FRAME_WIDTH = 320
    FRAME_HEIGHT = 240

    lower_red1 = np.array([0, 110, 70])
    upper_red1 = np.array([8, 255, 255])
    lower_red2 = np.array([165, 110, 70])
    upper_red2 = np.array([180, 255, 255])


    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()


    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        local_error = 999   # default = stop
        local_aruco_command = None


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

           
           
            # ================= ARUCO DETECTION =================
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            marker_id = ids[0][0]

            if marker_id == 0:
                local_command = 'L'
            elif marker_id == 1:
                local_command = 'R'
            elif marker_id == 2:
                local_command = 'F'
            else:
                local_command = None

            with lock:
                aruco_command = local_command
                aruco_last_time = time.time()

            cv2.putText(frame, f"Aruco ID: {marker_id}",
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0,255,0), 2)



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

    Kp = 0.5
    Ki = 0.0
    Kd = 0.2

    prev_error = 0
    integral = 0

    last_command = None

    while True:

        with lock:
            current_error = error
            current_aruco = aruco_command
            last_time = aruco_last_time

        # Priority: ArUco overrides tracking
        if current_aruco is not None and (time.time() - last_time) < 2:
            command = current_aruco
            integral = 0

        elif current_error == 999:
            command = 'S'
            integral = 0


        else:
            # PID calculations
            integral += current_error
            derivative = current_error - prev_error
            output = Kp*current_error + Ki*integral + Kd*derivative

            prev_error = current_error

            threshold = 15

            if output > threshold:
                command = 'R'
            elif output < -threshold:
                command = 'L'
            else:
                command = 'F'


        if command != last_command:
            send_to_rpi(command)
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

