# Import the robotar package
from pybotarena import RobotAR, PlatformAR

# Create a robot connection which requires 3 parameters found in the game
# The first parameter is the game ip address, second is port number and third is player id (0 to 3)
robot = RobotAR("10.19.27.227", 49156, 0)

# Keep looping until robot is standing on the platform delta number that does not match 'none' code.
while robot.get_prox_ground().delta[0] == PlatformAR.platform_code['none'] or \
robot.get_prox_ground().delta[1] == PlatformAR.platform_code['none']:
    # Ask the robot to start walking forward by 100 in left and right wheel
    robot.wheels(100,100)
    # Let the robot run for 1 seconds
    robot.sleep(1)
    # Ask the robot to stop
    robot.halt()

# Check the ground if it is standing on the platform delta number matches 'exit' code.
if robot.get_prox_ground().delta[0] == PlatformAR.platform_code['exit'] or \
robot.get_prox_ground().delta[1] == PlatformAR.platform_code['exit']:
    # Use the platform if standing on exit
    robot.use_platform()
else:
    # Print the delta number for debugging
    print(robot.get_prox_ground().delta)
