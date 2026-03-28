import math

# Robot pose (from Part B final step)
x = float(input("Robot x position: "))
y = float(input("Robot y position: "))
theta = float(input("Robot orientation (rad): "))

# Point in robot frame
xr = float(input("Point x in robot frame: "))
yr = float(input("Point y in robot frame: "))

# Transformation
xw = x + xr * math.cos(theta) - yr * math.sin(theta)
yw = y + xr * math.sin(theta) + yr * math.cos(theta)


# Output
print(f"World Frame Point: x={xw:.2f}, y={yw:.2f}")