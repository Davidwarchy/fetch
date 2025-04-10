from controller import Robot, Keyboard

# Create the Robot instance
robot = Robot()

# Get the time step of the current world
timestep = int(robot.getBasicTimeStep())

# Enable keyboard
keyboard = Keyboard()
keyboard.enable(timestep)

# Motor names for the wheels
wheel_motors = {
    "r_wheel_joint": robot.getDevice("r_wheel_joint"),
    "l_wheel_joint": robot.getDevice("l_wheel_joint")
}

# Initialize motors for velocity control
for motor in wheel_motors.values():
    motor.setPosition(float('inf'))  # Set to velocity control mode
    motor.setVelocity(0.0)

# Movement parameters
max_wheel_velocity = 5.0  # rad/s (adjust based on testing)

def process_keyboard():
    """Process keyboard input and return movement commands"""
    key = keyboard.getKey()
    
    forward = 0.0
    turn = 0.0
    
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
    
    return forward, turn

def set_wheel_velocities(forward, turn):
    """Set differential drive velocities"""
    left_velocity = (forward - turn) * max_wheel_velocity
    right_velocity = (forward + turn) * max_wheel_velocity
    
    wheel_motors["l_wheel_joint"].setVelocity(left_velocity)
    wheel_motors["r_wheel_joint"].setVelocity(right_velocity)

# Main control loop
print("Base movement controller started. Use WASD keys to move the robot.")
print("W: Forward, S: Backward, A: Turn Left, D: Turn Right")

while robot.step(timestep) != -1:
    # Get keyboard input
    forward, turn = process_keyboard()
    
    # Handle base movement
    set_wheel_velocities(forward, turn)