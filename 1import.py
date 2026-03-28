import math
import matplotlib.pyplot as plt

# Initial state
x, y, theta = 0.0, 0.0, 0.0

v = 0.63
omega = 0.33
dt = 0.1

# Store trajectory
x_points = []
y_points = []

for step in range(10):   # as per question
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt
    theta += omega * dt

    x_points.append(x)
    y_points.append(y)

    # Print pose
    print(f"Step {step+1}: x = {x:.3f}, y = {y:.3f}, theta = {theta:.3f}")

# Plot trajectory
plt.figure()
plt.plot(x_points, y_points, marker='o')
plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.title("Robot Trajectory")
plt.grid()
plt.axis("equal")
plt.show()