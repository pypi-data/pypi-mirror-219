from robotar import RobotAR

#robot = RobotAR("10.19.113.163", 50107, 0)
robot = RobotAR("10.19.69.124", 54987, 0)
#robot = RobotAR("10.19.125.85", 50140, 0)

#robot1 = RobotAR("10.19.113.163", 50107, 1)
robot1 = RobotAR("10.19.69.124", 54987, 1)
#robot1 = RobotAR("10.19.125.85", 50140, 1)

for x in range(3):
    robot.wheels(100,100)
    robot.sleep(2.8)
    robot.halt()
    if robot.get_prox_ground().delta[0] == robot.platformCode['item'] or robot.get_prox_ground().delta[1] == robot.platformCode['item']:
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)

    robot1.wheels(100,100)
    robot1.sleep(2.8)
    robot1.halt()
    if robot1.get_prox_ground().delta[0] == robot1.platformCode['item'] or robot1.get_prox_ground().delta[1] == robot1.platformCode['item']:
        robot1.use_platform()
    else:
        print(robot1.get_prox_ground().delta)
    robot1.wheels(100,100)
    robot1.sleep(2.8)
    robot1.halt()
    if robot1.get_prox_ground().delta[0] == robot1.platformCode['crafting'] or robot1.get_prox_ground().delta[1] == robot1.platformCode['crafting']:
        robot1.use_platform()
    else:
        print(robot1.get_prox_ground().delta)

    robot.wheels(100,100)
    robot.sleep(2.8)
    robot.halt()
    if robot.get_prox_ground().delta[0] == robot.platformCode['crafting'] or robot.get_prox_ground().delta[1] == robot.platformCode['crafting']:
        robot.use_platform()
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)
    robot.wheels(100,100)
    robot.sleep(2.5)
    robot.halt()
    if robot.get_prox_ground().delta[0] == robot.platformCode['launch'] or robot.get_prox_ground().delta[1] == robot.platformCode['launch']:
        robot.use_platform()
    else:
        print(robot.get_prox_ground().delta)
    robot.wheels(-100,-100)
    robot.sleep(8.3)
    robot.halt()

    robot1.wheels(-100,-100)
    robot1.sleep(6)
    robot1.halt()

robot.wheels(100,100)
robot.sleep(17)
robot.halt()
if robot.get_prox_ground().delta[0] == robot.platformCode['exit'] or robot.get_prox_ground().delta[1] == robot.platformCode['exit']:
    robot.use_platform()
else:
    print(robot.get_prox_ground().delta)

# 3 > 3 > 3

'''
robot.wheels(100,100)
robot.sleep(5)
print(robot.get_wheels())
print(robot.get_rotation())
robot.set_other_inputs(True, True, False, True, False)
robot.leds_circle(0, 0, 32, 0, 0, 0, 0, 0)
robot.leds_top(32, 32, 0)
print(robot.get_prox_horizontal())
print(robot.get_prox_ground())
print(robot.get_accelerometer())
print(robot.get_button_center())
print(robot.get_button_left())
print(robot.get_button_right())
print(robot.get_button_forward())
print(robot.get_button_backward())
robot.use_platform()
robot.get_player_item()
robot.dump_player_item()
robot.halt()
'''