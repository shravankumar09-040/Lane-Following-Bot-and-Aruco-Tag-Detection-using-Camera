import math

x, y, theta = 0, 0, 0
v = float(input("Enter linear velocity (m/s): "))
omega = float(input("Enter angular velocity (rad/s): "))
dt = 0.1

for i in range(5):
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt
    print(f"Pose {i+1}: x={x:.2f}, y={y:.2f}, theta={theta:.2f}")
