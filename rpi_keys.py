#!/usr/bin/env python3
import sys, termios, tty, serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
print("Keyboard Control: F B L R S  |  Press Q to quit")

def send(cmd):
    print("Sending:", cmd)
    ser.write(cmd.encode())

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

while True:
    key = getch().upper()

    if key in ['F', 'B', 'L', 'R', 'S']:
        send(key)

    elif key == 'Q':
        send("S")
        print("\nQuit")
        break
