# Import the robotar package
from pybotarena import RobotAR, PlatformAR

# Create move function so you do not need to spam ctrl+c and ctrl+v
# Parameter r is for the robot
def move_forward_or_backward_till_step_on_platform(r, move_forward):
    # Keep looping until robot is standing on the platform delta number that does not match 'none' code.
    while r.get_prox_ground().delta[0] == PlatformAR.platform_code['none'] or \
    r.get_prox_ground().delta[1] == PlatformAR.platform_code['none']:
        # Ask the robot to start walking forward or backwards by 100 in left and right wheel
        if move_forward:
            r.wheels(100,100)
        else:
            r.wheels(-100,-100)
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

# Method to get the robot in r to go in and out a teleport platform
def teleport_in_and_out(r):
    check_ground_and_use_it(r, PlatformAR.platform_code['teleport'])
    r.wheels(100,100)
    r.sleep(3)
    r.wheels(-100,-100)
    r.sleep(3)
    r.halt()
    check_ground_and_use_it(r, PlatformAR.platform_code['teleport'])

# Method to get the robot in r to keep moving till it matches the platform_delta
# the move_forward parameter is True for going forward and False for going backward
def keep_moving_till_floor_is_correct_and_use_it(r, move_forward, platform_delta):
    while not check_ground_and_use_it(r, platform_delta):
        # Move the robot forward abit because robot is currently stand on a platform and resume movement
        if move_forward:
            r.wheels(100,100)
        else:
            r.wheels(-100,-100)
        r.sleep(0.5)
        r.halt()
        move_forward_or_backward_till_step_on_platform(r, move_forward)

# Method to get 3 robots to cooperate and craft before firing weapon
def begin_3_cycle_enemy(r0, r1, r2):
    for x in range(3):
        # Start with getting the robot in r1 to deliver an item to the crafting platform and go back
        check_ground_and_use_it(r1, PlatformAR.platform_code['item'])
        keep_moving_till_floor_is_correct_and_use_it(r1, True, PlatformAR.platform_code['crafting'])
        keep_moving_till_floor_is_correct_and_use_it(r1, False, PlatformAR.platform_code['item'])
        r1.dump_player_item()

        # Followed with getting the robot in r2 to deliver an item to the crafting platform and go back
        check_ground_and_use_it(r2, PlatformAR.platform_code['item'])
        keep_moving_till_floor_is_correct_and_use_it(r2, True, PlatformAR.platform_code['crafting'])
        keep_moving_till_floor_is_correct_and_use_it(r2, False, PlatformAR.platform_code['item'])
        r2.dump_player_item()

        # Ending  with getting the robot in r0 to deliver the crafted item to the launch platform and fire it before returning.
        check_ground_and_use_it(r0, PlatformAR.platform_code['crafting'])
        keep_moving_till_floor_is_correct_and_use_it(r0, False, PlatformAR.platform_code['teleport'])
        keep_moving_till_floor_is_correct_and_use_it(r0, True, PlatformAR.platform_code['launch'])
        keep_moving_till_floor_is_correct_and_use_it(r0, False, PlatformAR.platform_code['teleport'])
        keep_moving_till_floor_is_correct_and_use_it(r0, True, PlatformAR.platform_code['crafting'])
        r0.dump_player_item()

# Create a robot connection which requires 3 parameters found in the game
# The first parameter is the game ip address, second is port number and third is player id (0 to 3)
robot = RobotAR("10.19.27.227", 54996, 0)
# For this example we would be taking turns controlling all the player robots
robot1 = RobotAR("10.19.27.227", 54996, 1)
robot2 = RobotAR("10.19.27.227", 54996, 2)
robot3 = RobotAR("10.19.27.227", 54996, 3)

# Move robot to its starting position
# Rotate the robot towards the teleport platform
rotate_robot(robot, True, 10)
# Get robot to move and use the teleport platform
keep_moving_till_floor_is_correct_and_use_it(robot, True, PlatformAR.platform_code['teleport'])
# Call the teleport_in_and_out method  for the robot
teleport_in_and_out(robot)
# Get the robot to the starting position
keep_moving_till_floor_is_correct_and_use_it(robot, True, PlatformAR.platform_code['crafting'])

# Move robot2 to its starting position
rotate_robot(robot2, False, 20)
move_forward_or_backward_till_step_on_platform(robot2, True)

# Move robot1 to its starting position
rotate_robot(robot1, False, 70)
robot1.wheels(100,100)
robot1.sleep(3)
robot1.halt()
rotate_robot(robot1, True, 85)
move_forward_or_backward_till_step_on_platform(robot1, True)

# Call the begin_3_cycle_enemy method using robot as the delivering to launcher and robot1/robot2 to make the crafted item
begin_3_cycle_enemy(robot, robot1, robot2)

# Move robot to its new starting position
rotate_robot(robot, False, 120)
move_forward_or_backward_till_step_on_platform(robot, True)
teleport_in_and_out(robot)
keep_moving_till_floor_is_correct_and_use_it(robot, True, PlatformAR.platform_code['crafting'])

# Move robot2 to its new starting position
rotate_robot(robot2, True, 45)
move_forward_or_backward_till_step_on_platform(robot2, False)

# Move robot3 to its starting position
move_forward_or_backward_till_step_on_platform(robot3, True)
rotate_robot(robot3, False, 10)

# Call the begin_3_cycle_enemy method using robot as the delivering to launcher and robot2/robot3 to make the crafted item
begin_3_cycle_enemy(robot, robot2, robot3)

# Move robot to the exit
keep_moving_till_floor_is_correct_and_use_it(robot, False, PlatformAR.platform_code['teleport'])
rotate_robot(robot, False, 10)
keep_moving_till_floor_is_correct_and_use_it(robot, True, PlatformAR.platform_code['exit'])
