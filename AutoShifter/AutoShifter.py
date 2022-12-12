import ac
import acsys
import time
import sys
import os
import platform

if platform.architecture()[0] == "64bit":
    sysdir = os.path.dirname(__file__) + '/stdlib64'
else:
    sysdir = os.path.dirname(__file__) + '/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."
import keyboard
from sim_info import info

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
debug = True
m_rpm = info.static.maxRpm
timer = time.perf_counter()


def acMain(ac_version):
    app = ac.newApp("Auto Shifter")
    ac.setSize(app, x_app, y_app)
    if debug:
        global show_gear, show_rpm, show_gas, show_brake, show_speed, show_m_rpm, show_mode

        show_gear = ac.addLabel(app, "Gear: ")
        ac.setPosition(show_gear, 3, 30)

        show_m_rpm = ac.addLabel(app, "Max rpm: ")
        ac.setPosition(show_m_rpm, 3, 60)

        show_rpm = ac.addLabel(app, "RPM: ")
        ac.setPosition(show_rpm, 3, 90)

        show_gas = ac.addLabel(app, "Gas: ")
        ac.setPosition(show_gas, 3, 120)

        show_brake = ac.addLabel(app, "Brake: ")
        ac.setPosition(show_brake, 3, 150)

        show_mode = ac.addLabel(app, "Last_mode: ")
        ac.setPosition(show_mode, 3, 180)
    return "Auto Shifter"


def acUpdate(deltaT):
    global timer
    gear = ac.getCarState(0, acsys.CS.Gear)
    rpm = ac.getCarState(0, acsys.CS.RPM)
    gas = ac.getCarState(0, acsys.CS.Gas)
    brake = ac.getCarState(0, acsys.CS.Brake)

    if on:
        if gas <= 0.95:
            if rpm >= 3200 and gear > 1 and brake < 0.8 and time.perf_counter() - timer > 1:
                timer = time.perf_counter()
                keyboard.send('shift')
                if debug:
                    ac.setText(show_mode, "Last_mode:1.shift")
            elif rpm < 1500 and gear > 2:
                timer = time.perf_counter()
                keyboard.send('ctrl')
                if debug:
                    ac.setText(show_mode, "Last_mode:1.ctrl")
        elif 0.95 < gas:
            if rpm >= m_rpm * 0.95 and gear > 1 and brake < 0.8 and time.perf_counter() - timer > 1:
                timer = time.perf_counter()
                keyboard.send('shift')
                if debug:
                    ac.setText(show_mode, "Last_mode:2.shift")
            elif rpm < 4000 and gear > 2:
                if not (gas == 1 and gear == 3):
                    timer = time.perf_counter()
                    keyboard.send('ctrl')
                    if debug:
                        ac.setText(show_mode, "Last_mode:2.ctrl")

    if debug:
        ac.setText(show_gear, "Gear: {}".format(gear))
        ac.setText(show_rpm, "RPM: {}".format(rpm))
        ac.setText(show_m_rpm, "Max rpm: {}".format(m_rpm))
        ac.setText(show_gas, "Gas: {}".format(gas))
        ac.setText(show_brake, "Brake: {}".format(brake))
