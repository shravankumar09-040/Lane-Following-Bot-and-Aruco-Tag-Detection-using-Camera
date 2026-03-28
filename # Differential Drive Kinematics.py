# Differential Drive Kinematics

r = 0.05   # wheel radius (m)
L = 0.3    # distance between wheels (m)

wl = float(input("Enter left wheel speed (rad/s): "))
wr = float(input("Enter right wheel speed (rad/s): "))

v = r * (wr + wl) / 2
omega = r * (wr - wl) / L

print(f"Linear Velocity v = {v:.2f} m/s")
print(f"Angular Velocity ω = {omega:.2f} rad/s")

if wl == wr:
    print("Robot moves straight")
elif wl < wr:
    print("Robot turns left")
elif wl > wr:
    print("Robot turns right")
