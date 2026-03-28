import math

dt = 0.1

def simulate(v, omega, case_name):
    print(f"\n--- {case_name} ---")
    x, y, theta = 0, 0, 0

    for i in range(5):
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += omega * dt

        print(f"Step {i+1}: x={x:.2f}, y={y:.2f}, theta={theta:.2f}")

# Case 1: Straight motion (ω = 0)
simulate(v=0.5, omega=0.0, case_name="Case 1: Straight Motion")

# Case 2: Rotation in place (v = 0)
simulate(v=0.0, omega=0.5, case_name="Case 2: Rotation in Place")

# Case 3: Curved motion (v ≠ 0 and ω ≠ 0)
simulate(v=0.5, omega=0.5, case_name="Case 3: Curved Motion")