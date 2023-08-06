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


# Create a robot connection which requires 3 parameters found in the game
# The first parameter is the game ip address, second is port number and third is player id (0 to 3)
robot = RobotAR("10.19.27.227", 54095, 0)

# Get robot to move and use the item platform
move_forward_till_step_on_platform(robot)
check_ground_and_use_it(robot, PlatformAR.platform_code['item'])

# Store the rotation you want to be facing
destinationRotation = float(robot.get_rotation()) - 55
# Correct rotation if outside boundary
if destinationRotation >= 360:
    destinationRotation -= 360
elif destinationRotation < 0:
    destinationRotation += 360
# Rotate till the rotation value is at the destination rotation but with a 10 degree margin of error
while not destinationRotation - 5 < float(robot.get_rotation()) < destinationRotation + 5:
    # Ask the robot to start rotating left
    robot.wheels(0,1)
    # Let the robot rotate for 0.1 seconds
    robot.sleep(0.1)
    # Ask the robot to stop so that the robot can check rotation value
    robot.halt()

# Move the robot forward abit because robot is currently stand on a platform
robot.wheels(100,100)
robot.sleep(2)
robot.halt()

# Get robot to move and use the exit platform
move_forward_till_step_on_platform(robot)
check_ground_and_use_it(robot, PlatformAR.platform_code['exit'])

