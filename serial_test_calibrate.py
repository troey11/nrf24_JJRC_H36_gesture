# -*- coding: utf-8 -*-
"""
Serial_test_with_aux.py

Mengontrol drone via serial ke Arduino Uno pakai nRF24L01.
Sekarang dilengkapi akses ke AUX6 dan AUX7!

- Tombol panah: elevator & aileron (maju/mundur, kiri/kanan)
- w/s: throttle (naik/turun)
- a/d: rudder (yaw)
- 6: AUX6 (kalibrasi Y, pitch trim, RTH, 360 flip)
- 7: AUX7 (kalibrasi X, roll trim)

@author: perrytsao (dimodifikasi)
"""

import serial, time, msvcrt

throttle = 1000
aileron = 1500
elevator = 1500
rudder = 1500
aux6 = 0
aux7 = 0

tg = 10
ag = 50
eg = 50
rg = 50

try:
    arduino = serial.Serial('COM17', 115200, timeout=.01)
    time.sleep(1)
    
    while True:
        data = arduino.readline()
        if data:
            print "[AU]: " + data
        
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 27:  # ESC
                print "[PC]: ESC exiting"
                break
            elif key == 13:  # Enter
                print "[PC]: Enter"
            elif key == 119:  # w
                throttle += tg
            elif key == 97:  # a
                rudder -= rg
            elif key == 115:  # s
                throttle -= tg
            elif key == 100:  # d
                rudder += rg
            elif key == 54:  # '6'
                aux6 = 1 if aux6 == 0 else 0
                print "[PC]: AUX6 toggled ->", aux6
            elif key == 55:  # '7'
                aux7 = 1 if aux7 == 0 else 0
                print "[PC]: AUX7 toggled ->", aux7
            elif key == 224:
                key = ord(msvcrt.getch())
                if key == 80:  # Down arrow
                    elevator -= eg
                elif key == 72:  # Up arrow
                    elevator += eg
                elif key == 77:  # Right arrow
                    aileron += ag
                elif key == 75:  # Left arrow
                    aileron -= ag

            command = "%i,%i,%i,%i,%i,%i" % (throttle, aileron, elevator, rudder, aux6, aux7)
            print "[PC]: " + command
            arduino.write(command + "\n")

finally:
    arduino.close()
    arduino = serial.Serial('COM17', 115200, timeout=.01)
    arduino.close()
