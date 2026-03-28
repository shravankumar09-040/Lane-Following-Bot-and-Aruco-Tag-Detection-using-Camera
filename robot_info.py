robot_name = input("Enter robot name: ")
battery = int(input("Enter battery percentage: "))

if battery >= 50:
    print(robot_name, ": Robot is ready to move")
else:
    print(robot_name, ": Low battery, please charge")