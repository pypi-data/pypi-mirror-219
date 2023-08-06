from pybotarena import RobotAR, PlatformAR

robot = RobotAR("10.19.146.151", 49635, 0)
robot1 = RobotAR("10.19.146.151", 49635, 1)

for x in range(3):
    robot.wheels(100,100)
    robot.sleep(2.5)
    robot.halt()
    if robot.get_prox_ground().delta[0] == PlatformAR.platform_code['item'] or robot.get_prox_ground().delta[1] == PlatformAR.platform_code['item']:
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)

    robot1.wheels(100,100)
    robot1.sleep(2.5)
    robot1.halt()
    if robot1.get_prox_ground().delta[0] == PlatformAR.platform_code['item'] or robot1.get_prox_ground().delta[1] == PlatformAR.platform_code['item']:
        robot1.use_platform()
    else:
        print(robot1.get_prox_ground().delta)
    robot1.wheels(100,100)
    robot1.sleep(2.5)
    robot1.halt()
    if robot1.get_prox_ground().delta[0] == PlatformAR.platform_code['crafting'] or robot1.get_prox_ground().delta[1] == PlatformAR.platform_code['crafting']:
        robot1.use_platform()
    else:
        print(robot1.get_prox_ground().delta)

    robot.wheels(100,100)
    robot.sleep(2.5)
    robot.halt()
    if robot.get_prox_ground().delta[0] == PlatformAR.platform_code['crafting'] or robot.get_prox_ground().delta[1] == PlatformAR.platform_code['crafting']:
        robot.use_platform()
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)
    robot.wheels(100,100)
    robot.sleep(3.2)
    robot.halt()
    if robot.get_prox_ground().delta[0] == PlatformAR.platform_code['launch'] or robot.get_prox_ground().delta[1] == PlatformAR.platform_code['launch']:
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)
    robot.wheels(-100,-100)
    robot.sleep(8.4)
    robot.halt()

    robot1.wheels(-100,-100)
    robot1.sleep(5.2)
    robot1.halt()

robot.wheels(100,100)
robot.sleep(17.2)
robot.halt()
if robot.get_prox_ground().delta[0] == PlatformAR.platform_code['exit'] or robot.get_prox_ground().delta[1] == PlatformAR.platform_code['exit']:
    robot.use_platform()
else:
    print(robot.get_prox_ground().delta)
