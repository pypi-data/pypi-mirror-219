__author__ = 'reyn_app_igniter and chung zhi wei' 
'''
PybotARena module

'''

import time
import socket

class PlatformAR:
    platform_code = dict([
        ('none', 819),
        ('path', 842),
        ('item', 160),
        ('crafting', 240),
        ('launch', 320),
        ('teleport', 762),
        ('exit', 681)
    ])


class RobotAR:

    _identity = 0
    _ip = socket.gethostbyname(socket.gethostname())
    _port = 0

    def __init__(self, i, p, r):
        self._identity = r
        self._ip = i
        self._port = p
        self.__send_message(self._identity, "online()")

    def __send_message(self, id, msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._ip, self._port))
            compiled = str(id) + " " + msg
            s.send(compiled.encode())
            response_data = s.recv(1024).decode()
            s.close()
            return response_data
        except:
            print("Instructions cannot be sent. Please check unity address with yours.")
            return("Error")

    def wheels(self, lv, rv):
        self.__send_message(self._identity, "wheels(" + str(lv) + "," + str(rv) + ")")
        #unity.u3dwheels(leftv, rightv)

    def get_wheels(self):
        result = self.__send_message(self._identity, "get_wheels()")
        if result == "Error":
            return "Error"
        output = result.split(',')
        leftv = float(output[0])
        rightv = float(output[1])
        return leftv, rightv

    def halt(self):
        self.wheels(0,0)
        
    def get_rotation(self):
        results = self.__send_message(self._identity, "get_rotation()")
        if results == "Error":
            return "Error"
        return results

    def get_player_item(self):
        results = self.__send_message(self._identity, "get_player_item()")
        if results == "Error":
            return "Error"
        return results

    def dump_player_item(self):
        self.__send_message(self._identity, "dump_player_item()")

    def use_platform(self):
        self.__send_message(self._identity, "use_platform()")

    def reset(self):
        self.__send_message(self._identity, "reset()")

    def sleep(self, sec):
        time.sleep(sec)

    #def set_other_inputs(self, temp_val, btn_center_val, btn_left_val, btn_right_val, btn_forward_val, btn_backward_val):
    #    temperature = temp_val
    #    btn_center = btn_center_val
    #    btn_left = btn_left_val
    #    btn_right = btn_right_val
    #    btn_forward = btn_forward_val
    #    btn_backward = btn_backward_val

    def set_other_inputs(self, btn_center_val, btn_left_val, btn_right_val, btn_forward_val, btn_backward_val):
         self.__send_message(self._identity, "set_other_inputs(" + str(btn_center_val) + "," + str(btn_left_val) + 
                      "," + str(btn_right_val) + "," + str(btn_forward_val) + "," + str(btn_backward_val) + ")")

    def leds_circle(self, led0, led1, led2, led3, led4, led5, led6, led7):
        self.__send_message(self._identity, "leds_circle(" + str(led0) 
                   + "," + str(led1) + "," + str(led2) 
                   + "," + str(led3) + "," + str(led4) 
                   + "," + str(led5) + "," + str(led6) 
                   + "," + str(led7) + ")")
        #u3dcircleleds(led0, led1, led2, led3, led4, led5, led6, led7)

    def leds_top(self, r, g, b):
        self.__send_message(self._identity, "leds_top(" + str(r) + "," + str(g) + "," + str(b)+ ")")
        #u3dtopleds(r, g, b)

    def use_platform(self):
        self.__send_message(self._identity, "use_platform()")

    def get_prox_horizontal(self):
        results = self.__send_message(self._identity, "get_prox_horizontal()")
        if results == "Error":
            return "Error"
        output = results.split(',')
        prox_horizontal = [int(output[0]), int(output[1]), int(output[2]), int(output[3]), int(output[4]), int(output[5]), int(output[6])]
        #prox_horizontal = [u3dgetproxhorizontal0(), u3dgetproxhorizontal1(), u3dgetproxhorizontal2(), u3dgetproxhorizontal3(), u3dgetproxhorizontal4(), u3dgetproxhorizontal5(), u3dgetproxhorizontal6()]
        return prox_horizontal

    def get_prox_ground(self):
        results = self.__send_message(self._identity, "get_prox_ground()")
        if results == "Error":
            return "Error"
        output = results.split(',')
        prox_ground = ProxGround([int(output[0]), int(output[1])], [int(output[2]), int(output[3])], [int(output[4]), int(output[5])])
        #prox_ground = ProxGround([u3dgetproxground0(), u3dgetproxground1()],[u3dgetproxground2(), u3dgetproxground3()],[u3dgetproxground4(), u3dgetproxground5()])
        return prox_ground

    def get_prox_frontground(self):
        results = self.__send_message(self._identity, "get_prox_frontground()")
        if results == "Error":
            return "Error"
        output = results.split(',')
        prox_ground = ProxGround([int(output[0]), int(output[1])], [int(output[2]), int(output[3])], [int(output[4]), int(output[5])])
        #prox_ground = ProxGround([u3dgetproxground0(), u3dgetproxground1()],[u3dgetproxground2(), u3dgetproxground3()],[u3dgetproxground4(), u3dgetproxground5()])
        return prox_ground

    #def temperature(self):
        #return u3dgettemperature()

    def get_accelerometer(self):
        results = self.__send_message(self._identity, "get_accelerometer()")
        if results == "Error":
            return "Error"
        output = results.split(',')
        return [int(output[0]), int(output[1]), int(output[2])]
        #return [u3dgetaccelerometerx(), u3dgetaccelerometery(), u3dgetaccelerometerz()]

    def get_button_center(self):
        results = self.__send_message(self._identity, "get_button_center()")
        if results == "Error":
            return "Error"
        return results == "True"
        #return u3dgetbtncenter()

    def get_button_left(self):
        results = self.__send_message(self._identity, "get_button_left()")
        if results == "Error":
            return "Error"
        return results == "True"
        #return u3dgetbtnleft()

    def get_button_right(self):
        results = self.__send_message(self._identity, "get_button_right()")
        if results == "Error":
            return "Error"
        return results == "True"
        #return u3dgetbtnright()

    def get_button_forward(self):
        results = self.__send_message(self._identity, "get_button_forward()")
        if results == "Error":
            return "Error"
        return results == "True"
        #return u3dgetbtnforward()

    def get_button_backward(self):
        results = self.__send_message(self._identity, "get_button_backward()")
        if results == "Error":
            return "Error"
        return results == "True"
        #return u3dgetbtnbackward()

    #@property
    #def init_pos(self):
        #return init_pos

    #@init_pos.setter
    #def init_pos(self, val):
        #init_pos = val


class ProxGround(object):
    def __init__(self,delta=[0,0],reflected=[0,0],ambiant=[0,0]):
        self.delta=delta
        self.reflected=reflected
        self.ambiant=ambiant

    def __str__(self):
        return "This is a ProxGround class."
