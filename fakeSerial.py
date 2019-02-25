import serial
import time

with serial.Serial('COM10', 115200) as ser:
    while (True):
        ser.write(0)
        print(0)
        time.sleep(1)
