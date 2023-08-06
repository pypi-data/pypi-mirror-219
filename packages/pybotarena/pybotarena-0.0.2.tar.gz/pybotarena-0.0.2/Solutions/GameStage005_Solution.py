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
        # Return true if using platform
        return True
    else:
        # Print the delta number for debugging
        print(r.get_prox_ground().delta)
        # Return false if not using platform
        return False

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
robot = RobotAR("10.19.27.227", 54820, 0)
robot1 = RobotAR("10.19.27.227", 54820, 1)
robot2 = RobotAR("10.19.27.227", 54820, 2)

# Create an array for the robots and the modified parameter for each loop
robot_array = [robot, robot1, robot2]
robot_rotate_bool = [False, True, True]
robot_rotate_amount = [25, 35, 25]

# Move 3 robots with an ammo to attack enemy
for x in range(3):
    # Rotate the robot towards the teleport
    rotate_robot(robot_array[x], robot_rotate_bool[x], robot_rotate_amount[x])

    # Get robot to move and use the teleport platform
    move_forward_till_step_on_platform(robot_array[x])
    # Redo movement if the platform the robot stand on is not the teleport platform
    while not check_ground_and_use_it(robot_array[x], PlatformAR.platform_code['teleport']):
        # Move the robot forward abit because robot is currently stand on a platform and resume movement
        robot_array[x].wheels(100,100)
        robot_array[x].sleep(2.5)
        robot_array[x].halt()
        move_forward_till_step_on_platform(robot_array[x])

    # Move the robot forward abit because robot is currently stand on a platform
    robot_array[x].wheels(100,100)
    robot_array[x].sleep(2.5)
    robot_array[x].halt()

    # Get robot to move and use the launch platform
    move_forward_till_step_on_platform(robot_array[x])
    check_ground_and_use_it(robot_array[x], PlatformAR.platform_code['launch'])

    # Reset the robot to move it away from the launch site
    if x < 2:
        robot_array[x].reset()
    else:
        # Get the last robot to move to the exit
        robot_array[x].wheels(100,100)
        robot_array[x].sleep(3)
        robot_array[x].halt()
        move_forward_till_step_on_platform(robot_array[x])
        check_ground_and_use_it(robot_array[x], PlatformAR.platform_code['exit'])
