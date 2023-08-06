# Import the robotar package
from pybotarena import RobotAR, PlatformAR

# Create move function so you do not need to spam ctrl+c and ctrl+v
# Parameter r is for the robot
def move_forward_till_step_on_platform(r):
    # Keep looping until robot is standing on the platform delta number that does not match 'none' code.
    while r.get_prox_ground().delta[0] == PlatformAR.platform_code['none'] or \
    r.get_prox_ground().delta[1] == PlatformAR.platform_code['none']:
        # Ask the robot to start walking forward by 100 in left and right wheel
        r.wheels(100,100)
        # Let the robot run for 0.1 seconds
        r.sleep(0.1)
        # Ask the robot to stop so that the robot can check platform without moving out of platform
        r.halt()

# Create a function to check the ground. 
# Parameter r is for the robot and parameter platform is the platform delta number
def check_ground_and_use_it(r, platform_delta):
    # Check the ground if it is standing on the platform delta number matches platform_delta.
    if r.get_prox_ground().delta[0] == platform_delta or \
    r.get_prox_ground().delta[1] == platform_delta:
        # Use the platform if standing on platform
        r.use_platform()
    else:
        # Print the delta number for debugging
        print(r.get_prox_ground().delta)

# Create a function to rotate the robot. 
# Parameter r is for the robot 
# Parameter rotate_right is a bool with true for right and false for left
# Parameter rotation_amount is a float of how much angle you want to adjust
def rotate_robot(r, rotate_right, rotation_amount):
    # Store the rotation you want to be facing
    destinationRotation = float(r.get_rotation())
    if rotate_right:
        # Add rotation_amount if rotating right
        destinationRotation += rotation_amount
        # Fix rotation if addition causes out of bounds
        if destinationRotation >= 360:
            destinationRotation -= 360
    else:
        # Subtract rotation_amount if rotating left
        destinationRotation -= rotation_amount
        # Fix rotation if subtraction causes out of bounds
        if destinationRotation < 0:
            destinationRotation += 360
    # Rotate till the rotation value is at the destination rotation but with a 10 degree margin of error
    while not destinationRotation - 5 < float(r.get_rotation()) < destinationRotation + 5:
        if rotate_right:
            # Ask the robot to start rotating right
            r.wheels(1,0)
        else:
            # Ask the robot to start rotating left
            r.wheels(0,1)
        # Let the robot rotate for 0.1 seconds
        r.sleep(0.1)
        # Ask the robot to stop so that the robot can check rotation value
        r.halt()

# Create a robot connection which requires 3 parameters found in the game
# The first parameter is the game ip address, second is port number and third is player id (0 to 3)
robot = RobotAR("10.19.27.227", 54095, 0)
robot3 = RobotAR("10.19.27.227", 54095, 3)

# Get robot to move and use the item platform
move_forward_till_step_on_platform(robot)
check_ground_and_use_it(robot, PlatformAR.platform_code['item'])

# Move the robot forward abit because robot is currently stand on a platform
robot.wheels(100,100)
robot.sleep(2.5)
robot.halt()

# Get robot to move and use the crafting platform
move_forward_till_step_on_platform(robot)
check_ground_and_use_it(robot, PlatformAR.platform_code['crafting'])

# Get robot3 to move and use the item platform
move_forward_till_step_on_platform(robot3)
check_ground_and_use_it(robot3, PlatformAR.platform_code['item'])

# Move the robot3 forward abit because robot is currently stand on a platform
robot3.wheels(100,100)
robot3.sleep(2.5)
robot3.halt()

# Get robot3 to move and use the crafting platform
move_forward_till_step_on_platform(robot3)
check_ground_and_use_it(robot3, PlatformAR.platform_code['crafting'])

# Get robot to collect the crafting result
check_ground_and_use_it(robot, PlatformAR.platform_code['crafting'])

# Rotate the robot towards the exit
rotate_robot(robot, False, 75)

# Move the robot forward abit because robot is currently stand on a platform
robot.wheels(100,100)
robot.sleep(2.5)
robot.halt()

# Get robot to move and use the exit platform
move_forward_till_step_on_platform(robot)
check_ground_and_use_it(robot, PlatformAR.platform_code['exit'])

