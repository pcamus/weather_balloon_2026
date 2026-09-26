# File : balloon2026_1_2.py
#
# This version only uses LPS22HB chip on the Pico 10-DOF IMU module
# Acceleratio is not recorded in this version.
#
# Log the temperature inside and outside the payload box, atmospheric pressure,
# battery voltage, and the current supplied by the battery
# Takes samples each 5 seconds
# Repeat the process during a specified time
#
# Append the data to csv file.
# Size : each period -> max 64 bytes. For 5s period -> 1 hour recording = 46080 bytes
#
# Power consumption 140 mWh per hour. Battery model 14500 = 2960 mWh -> +/- 20h of battery life
#
# Code was reviewed by Gemini AI and amended to increase reliability
# info@pcamus.be
# 24/09/2026

import machine
from machine import Pin
import onewire
import ds18x20
import time
import ina219
import lps22hb
import os

# -----------------------------------------------------------------------------
# General parameters
# -----------------------------------------------------------------------------
PERIOD = 5000         # sampling rate (in ms)
DURATION = 21600   # 21600 = 6 hour - total acquisition time (in seconds)
FILENAME = "balloon_data.csv"
CORR_PRESS = 1033/991  # calibration with IRM data

SAMPLES = DURATION // (PERIOD//1000)
print (SAMPLES)

# -----------------------------------------------------------------------------
# Heart beat and status LED
# -----------------------------------------------------------------------------
hb = Pin(25, Pin.OUT)
hb.off()

# -----------------------------------------------------------------------------
# DS18B20 initialization : temperature outside the payload
# ----------------------------------------------------------------------------
PIN_DATA = 22
ow = onewire.OneWire(Pin(PIN_DATA))
ds = ds18x20.DS18X20(ow)

ds_roms = ds.scan()

# --------------------------------------------------------------------------------
# LPS22HB initialization : atmospheric pressure and temperature inside the payload
# --------------------------------------------------------------------------------

lps22hb=lps22hb.LPS22HB() # uses I2C1

# --------------------------------------------------------------------------------
# INA219 initialization : battery voltage and current
# --------------------------------------------------------------------------------

bat_mon = ina219.INA219(addr=0x43) # uses I2C1

# Two blinks means all initializations succeeded
hb.on() 
time.sleep_ms(1000)
hb.off()
time.sleep_ms(1000)
hb.on() 
time.sleep_ms(1000)
hb.off()

# -----------------------------------------------------------------------------
# Opening and possible creation of data file on the flash - append mode
# First, write a header text for each column
# file will be formated as CSV
# ----------------------------------------------------------------------------
file_exists = True
try:
    os.stat(FILENAME)
except OSError:
    file_exists = False

if not file_exists:  # write column header if new file
    with open(FILENAME, "w") as f:
        f.write("Time;T_out;T_in;pressure;voltage;current\n")

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
start_mission_time = time.ticks_ms()
count = 0

while count < SAMPLES:
    cycle_start = time.ticks_ms()
    
    # LED fast flash  (Heartbeat)
    hb.on()
    time.sleep_ms(50)
    hb.off()
    
    # Elapsed time since the start of the mission
    elapsed_time = time.ticks_diff(cycle_start, start_mission_time) // 1000

    # call to DS18B20 sensor 
    str_T_out = "NC"
    if ds_roms:
        try:
            ds.convert_temp()
            time.sleep_ms(750)  # must wait a little lesss than 750 ms for 12-bit conversion
            T_out = ds.read_temp(ds_roms[0])
            str_T_out = f"{T_out:.1f}".replace('.', ',')
        except Exception as e:
            pass

    # call to LPS22HB chip (for inside temperature and pressure)
    try:
        pressure = lps22hb.pressure * CORR_PRESS
        T_in = lps22hb.temperature
        str_T_in = f"{T_in:.1f}".replace('.', ',')
        str_pressure = f"{pressure:.1f}".replace('.', ',')
    except Exception as e:
        str_T_in, str_pressure = "NC", "NC"
        

    # call to ina219 chip (for battery voltage and current)
    try:
        voltage = bat_mon.getBusVoltage_V()
        current = bat_mon.getCurrent_mA()
        str_voltage = f"{voltage:.3f}".replace('.', ',')
        str_current = f"{current:.3f}".replace('.', ',')
    except Exception as e:
        str_voltage, str_current = "NC", "NC"
        pass

    # Record data on flash memory
    try:
        with open(FILENAME, "a") as f:
            f.write(f"{elapsed_time};{str_T_out};{str_T_in};{str_pressure};{str_voltage};{str_current}\n")
    except OSError as e:
        pass

    count += 1

    # Compute remaining time to reach sample period
    elapsed_in_cycle = time.ticks_diff(time.ticks_ms(), cycle_start)
    remaining_sleep = PERIOD - elapsed_in_cycle
    
    if remaining_sleep > 0: # and sleep for the remaining time
        time.sleep_ms(remaining_sleep)

# Signal de fin (LED allumée 2 secondes)
hb.on()
time.sleep_ms(2000)
hb.off()
