import ac
import acsys
import keyboard
import time
import sys
import os
import platform
from sim_info import info

if platform.architecture()[0] == "64bit":
    sys_dir = "stdlib64"
else:
    sys_dir = "stdlib"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), sys_dir))
x_app = 200
y_app = 200

show_gear = 0
show_rpm = 0
show_gas = 0
show_brake = 0
show_speed = 0
show_m_rpm = 0
show_mode = 0

on = True
m_rpm = info.static.maxRpm
timer = time.perf_counter()
ctrl_time = 0


def acMain(ac_version):
    global show_gear, show_rpm, show_gas, show_brake, show_speed, show_m_rpm, show_mode

    app = ac.newApp("Auto Shifter")
    ac.setSize(app, x_app, y_app)

    show_gear = ac.addLabel(app, "Gear: ")
    ac.setPosition(show_gear, 3, 30)

    show_rpm = ac.addLabel(app, "RPM: ")
    ac.setPosition(show_rpm, 3, 60)

    show_m_rpm = ac.addLabel(app, "Max rpm: ")
    ac.setPosition(show_m_rpm, 90, 60)

    show_gas = ac.addLabel(app, "Gas: ")
    ac.setPosition(show_gas, 3, 90)

    show_brake = ac.addLabel(app, "Brake: ")
    ac.setPosition(show_brake, 3, 120)

    show_speed = ac.addLabel(app, "Speed: ")
    ac.setPosition(show_speed, 3, 150)

    show_mode = ac.addLabel(app, "Mode: ")
    ac.setPosition(show_mode, 3, 180)
    return "Auto Shifter"


def acUpdate(deltaT):
    global on, timer, ctrl_time
    gear = ac.getCarState(0, acsys.CS.Gear)
    ac.setText(show_gear, "Gear: {}".format(gear))

    rpm = ac.getCarState(0, acsys.CS.RPM)
    ac.setText(show_rpm, "RPM: {}".format(rpm))

    ac.setText(show_m_rpm, "Max rpm: {}".format(m_rpm))

    gas = ac.getCarState(0, acsys.CS.Gas)
    ac.setText(show_gas, "Gas: {}".format(gas))

    brake = ac.getCarState(0, acsys.CS.Brake)
    ac.setText(show_brake, "Brake: {}".format(brake))

    speed = ac.getCarState(0, acsys.CS.SpeedKMH)
    ac.setText(show_speed, "Speed: {}".format(speed))

    if on:
        if gas <= 0.95:
            if rpm >= 3000 and gear > 1 and brake < 0.8 and time.perf_counter() - timer > 1:
                timer = time.perf_counter()
                keyboard.send('shift')
                ac.setText(show_mode, "Mode:1.1")
            elif rpm < 2000 and gear > 2:
                ac.setText(show_mode, "gas = {}, gear = {}".format(gas != 1, gear != 3))
                if not (gas == 1 and gear == 3):
                    timer = time.perf_counter()
                    keyboard.send('ctrl')
                    ac.setText(show_mode, "Mode:1.2")
        elif 0.95 < gas:
            if rpm >= m_rpm * 0.95 and gear > 1 and brake < 0.8 and time.perf_counter() - timer > 1:
                timer = time.perf_counter()
                keyboard.send('shift')
                ac.setText(show_mode, "Mode:2.1")
            elif rpm < 4500 and gear > 2:
                if not (gas == 1 and gear == 3):
                    timer = time.perf_counter()
                    keyboard.send('ctrl')
                    ac.setText(show_mode, "Mode:2.2")
