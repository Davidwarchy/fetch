from controller import Robot, Motor, PositionSensor, Keyboard

# Create the Robot instance
robot = Robot()

# Get the time step of the current world
timestep = int(robot.getBasicTimeStep())

# Enable keyboard
keyboard = Keyboard()
keyboard.enable(timestep)

# Motor names from the Fetch PROTO file
wheel_motors = {
    "r_wheel_joint": robot.getDevice("r_wheel_joint"),
    "l_wheel_joint": robot.getDevice("l_wheel_joint")
}

torso_motor = robot.getDevice("torso_lift_joint")

arm_motors = {
    "shoulder_pan_joint": robot.getDevice("shoulder_pan_joint"),
    "shoulder_lift_joint": robot.getDevice("shoulder_lift_joint"),
    "upperarm_roll_joint": robot.getDevice("upperarm_roll_joint"),
    "elbow_flex_joint": robot.getDevice("elbow_flex_joint"),
    "forearm_roll_joint": robot.getDevice("forearm_roll_joint"),
    "wrist_flex_joint": robot.getDevice("wrist_flex_joint"),
    "wrist_roll_joint": robot.getDevice("wrist_roll_joint")
}

gripper_motors = {
    "r_gripper_finger_joint": robot.getDevice("r_gripper_finger_joint"),
    "l_gripper_finger_joint": robot.getDevice("l_gripper_finger_joint")
}

# Sensor names
wheel_sensors = {
    "r_wheel_joint_sensor": robot.getDevice("r_wheel_joint_sensor"),
    "l_wheel_joint_sensor": robot.getDevice("l_wheel_joint_sensor")
}

torso_sensor = robot.getDevice("torso_lift_joint_sensor")

arm_sensors = {
    "shoulder_pan_joint_sensor": robot.getDevice("shoulder_pan_joint_sensor"),
    "shoulder_lift_joint_sensor": robot.getDevice("shoulder_lift_joint_sensor"),
    "upperarm_roll_joint_sensor": robot.getDevice("upperarm_roll_joint_sensor"),
    "elbow_flex_joint_sensor": robot.getDevice("elbow_flex_joint_sensor"),
    "forearm_roll_joint_sensor": robot.getDevice("forearm_roll_joint_sensor"),
    "wrist_flex_joint_sensor": robot.getDevice("wrist_flex_joint_sensor"),
    "wrist_roll_joint_sensor": robot.getDevice("wrist_roll_joint_sensor")
}

gripper_sensors = {
    "r_gripper_finger_joint_sensor": robot.getDevice("r_gripper_finger_joint_sensor"),
    "l_gripper_finger_joint_sensor": robot.getDevice("l_gripper_finger_joint_sensor")
}

# Enable sensors
for sensor in wheel_sensors.values():
    sensor.enable(timestep)
torso_sensor.enable(timestep)
for sensor in arm_sensors.values():
    sensor.enable(timestep)
for sensor in gripper_sensors.values():
    sensor.enable(timestep)

# Movement parameters
max_wheel_velocity = 5.0  # rad/s (adjust based on testing)
max_torso_velocity = 0.1  # m/s
max_arm_velocity = 1.0    # rad/s
max_gripper_velocity = 0.05  # m/s

# Default positions
default_torso_position = 0.0
default_arm_positions = {
    "shoulder_pan_joint": 0.0,
    "shoulder_lift_joint": 0.0,
    "upperarm_roll_joint": 0.0,
    "elbow_flex_joint": 0.0,
    "forearm_roll_joint": 0.0,
    "wrist_flex_joint": 0.0,
    "wrist_roll_joint": 0.0
}
default_gripper_position = 0.0  # Open position

# Initialize motors to default positions
for motor in wheel_motors.values():
    motor.setPosition(float('inf'))  # Velocity control for wheels
    motor.setVelocity(0.0)

torso_motor.setPosition(default_torso_position)
torso_motor.setVelocity(max_torso_velocity)

for name, motor in arm_motors.items():
    motor.setPosition(default_arm_positions[name])
    motor.setVelocity(max_arm_velocity)

for motor in gripper_motors.values():
    motor.setPosition(default_gripper_position)
    motor.setVelocity(max_gripper_velocity)

def process_keyboard():
    """Process keyboard input and return movement commands"""
    key = keyboard.getKey()
    
    if key != -1:
        print(f"Key pressed: {key} (ASCII: {chr(key) if 32 <= key <= 126 else 'non-printable'})")
    
    forward = 0.0
    turn = 0.0
    torso_lift = 0.0
    reset = False
    shoulder_pan = 0.0
    shoulder_lift = 0.0
    elbow_flex = 0.0
    gripper_move = 0.0
    
    # WASD for base movement
    if key == ord("W") or key == ord("w"):
        forward = 1.0
        print("Moving forward")
    elif key == ord("S") or key == ord("s"):
        forward = -1.0
        print("Moving backward")
    elif key == ord("A") or key == ord("a"):
        turn = 1.0
        print("Turning left")
    elif key == ord("D") or key == ord("d"):
        turn = -1.0
        print("Turning right")
    
    # L for torso lift
    elif key == ord("L") or key == ord("l"):
        torso_lift = 0.38615  # Max torso height
        print("Lifting torso")
    
    # R to reset
    elif key == ord("R") or key == ord("r"):
        reset = True
        print("Resetting position")
    
    # Arm control (example: U, I, O, P)
    elif key == ord("U") or key == ord("u"):
        shoulder_pan = 0.1
        print("Shoulder pan right")
    elif key == ord("I") or key == ord("i"):
        shoulder_pan = -0.1
        print("Shoulder pan left")
    elif key == ord("O") or key == ord("o"):
        shoulder_lift = 0.1
        print("Shoulder lift up")
    elif key == ord("P") or key == ord("p"):
        shoulder_lift = -0.1
        print("Shoulder lift down")
    elif key == ord("K") or key == ord("k"):
        elbow_flex = 0.1
        print("Elbow flex up")
    elif key == ord("M") or key == ord("m"):
        elbow_flex = -0.1
        print("Elbow flex down")
    
    # Gripper control
    elif key == ord("G") or key == ord("g"):
        gripper_move = 0.05  # Close gripper
        print("Closing gripper")
    elif key == ord("H") or key == ord("h"):
        gripper_move = -0.05  # Open gripper
        print("Opening gripper")
    
    return forward, turn, torso_lift, reset, shoulder_pan, shoulder_lift, elbow_flex, gripper_move

def set_wheel_velocities(forward, turn):
    """Set differential drive velocities"""
    left_velocity = (forward - turn) * max_wheel_velocity
    right_velocity = (forward + turn) * max_wheel_velocity
    
    wheel_motors["l_wheel_joint"].setVelocity(left_velocity)
    wheel_motors["r_wheel_joint"].setVelocity(right_velocity)

def reset_position():
    """Reset robot to default position"""
    for motor in wheel_motors.values():
        motor.setVelocity(0.0)
    torso_motor.setPosition(default_torso_position)
    for name, motor in arm_motors.items():
        motor.setPosition(default_arm_positions[name])
    for motor in gripper_motors.values():
        motor.setPosition(default_gripper_position)

# Main control loop
print("Controller started. Use WASD to move, L to lift torso, R to reset, U/I for shoulder pan, O/P for shoulder lift, K/M for elbow flex, G/H for gripper.")

while robot.step(timestep) != -1:
    # Get keyboard input
    forward, turn, torso_lift, reset, shoulder_pan, shoulder_lift, elbow_flex, gripper_move = process_keyboard()
    
    # Reset to default position if requested
    if reset:
        reset_position()
        continue
    
    # Handle base movement
    if forward != 0 or turn != 0:
        set_wheel_velocities(forward, turn)
    else:
        set_wheel_velocities(0.0, 0.0)
    
    # Handle torso lift
    if torso_lift != 0:
        torso_motor.setPosition(torso_lift)
    elif not reset and torso_sensor.getValue() != default_torso_position:
        torso_motor.setPosition(default_torso_position)
    
    # Handle arm movement
    if shoulder_pan != 0:
        current_pos = arm_sensors["shoulder_pan_joint_sensor"].getValue()
        arm_motors["shoulder_pan_joint"].setPosition(current_pos + shoulder_pan)
    if shoulder_lift != 0:
        current_pos = arm_sensors["shoulder_lift_joint_sensor"].getValue()
        arm_motors["shoulder_lift_joint"].setPosition(current_pos + shoulder_lift)
    if elbow_flex != 0:
        current_pos = arm_sensors["elbow_flex_joint_sensor"].getValue()
        arm_motors["elbow_flex_joint"].setPosition(current_pos + elbow_flex)
    
    # Handle gripper movement
    if gripper_move != 0:
        current_pos_r = gripper_sensors["r_gripper_finger_joint_sensor"].getValue()
        current_pos_l = gripper_sensors["l_gripper_finger_joint_sensor"].getValue()
        new_pos_r = max(0.0, min(0.05, current_pos_r + gripper_move))
        new_pos_l = max(0.0, min(0.05, current_pos_l + gripper_move))
        gripper_motors["r_gripper_finger_joint"].setPosition(new_pos_r)
        gripper_motors["l_gripper_finger_joint"].setPosition(new_pos_l)
    
    # Debug output (optional)
    if robot.getTime() % 1.0 < timestep / 1000.0:  # Print once per second
        print(f"Torso height: {torso_sensor.getValue():.3f}, "
              f"Shoulder pan: {arm_sensors['shoulder_pan_joint_sensor'].getValue():.3f}")