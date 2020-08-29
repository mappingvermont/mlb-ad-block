#!/usr/bin/python3
# Modified from: https://www.piddlerintheroot.com/fm-radio-tea5767/
import smbus as smbus 
import subprocess
import time

I2C = smbus.SMBus(1) # newer version RASP (512 megabytes)
I2C_ADDRESS = 0x60
FREQUENCY = 106.7


def init_radio():
    """initialize hardware"""
    I2C.write_quick(I2C_ADDRESS)
    time.sleep(0.1)


def play():
    """Play radio at FREQUENCY defined in global var"""
    freq14bit = int (4 * (FREQUENCY * 1000000 + 225000) / 32768) # Frequency distribution for two bytes (according to the data sheet)
    freqH = freq14bit>>8 #int (freq14bit / 256)
    freqL = freq14bit & 0xFF

    data = [0 for i in range(4)] # Descriptions of individual bits in a byte - viz.  catalog sheets
    init = freqH # freqH # 1.bajt (MUTE bit; Frequency H)  // MUTE is 0x80
    data[0] = freqL # 2.bajt (frequency L)
    data[1] = 0xB0 #0b10110000 # 3.bajt (SUD; SSL1, SSL2; HLSI, MS, MR, ML; SWP1)
    data[2] = 0x10 #0b00010000 # 4.bajt (SWP2; STBY, BL; XTAL; smut; HCC, SNC, SI)
    data[3] = 0x00 #0b00000000 # 5.bajt (PLREFF; DTC; 0; 0; 0; 0; 0; 0)
    try:
      I2C.write_i2c_block_data (I2C_ADDRESS, init, data) # Setting a new frequency to the circuit
    except IOError:
      subprocess.call(['i2cdetect', '-y', '1'])


def mute():
    """"mute radio"""
    freq14bit = int(4 * (0 * 1000000 + 225000) / 32768)
    freqL = freq14bit & 0xFF
    data = [0 for i in range(4)]
    init = 0x80
    data[0] = freqL
    data[1] = 0xB0
    data[2] = 0x10
    data[3] = 0x00
    try:
        I2C.write_i2c_block_data(I2C_ADDRESS, init, data)
        print("Radio Muted")
    except IOError:
        subprocess.call(['i2cdetect', '-y', '1'])


if __name__ == '__main__':
    init_radio()
    mute()
