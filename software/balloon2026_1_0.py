# File : balloon2026_1_0.py
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
# Size : each period -> max 64 bytes. For 5s period -> 1 hour recording = 46080 byte
#
# Power consumption 140 mWh per hour. Battery model 14500 = 2960 mWh -> +/- 20h of battery life
#
# info@pcamus.be
# 18/09/2026


import machine
from machine import Pin
import onewire
import ds18x20
import time
import ina219
#import lps22hb.py

# -----------------------------------------------------------------------------
# General parameters
# -----------------------------------------------------------------------------
PERIOD = 5000         # sampling rate (in ms)
DURATION = 180   # total acquisition time (in seconds)
FILENAME = "balloon_data.csv"

SAMPLES = DURATION // (PERIOD//1000)

# -----------------------------------------------------------------------------
# Heart beat and status LED
# -----------------------------------------------------------------------------
hb = Pin(25, machine.Pin.OUT)
hb.off()

# -----------------------------------------------------------------------------
# DS18B20 initialization : temperature outside the payload
# -----------------------------------------------------------------------------
# PIN_DATA = 22           # DS18B20 on GP22
# ow = onewire.OneWire(Pin(PIN_DATA))
# ds = ds18x20.DS18X20(ow)
# 
# id = ds.scan()  # we have just one sensor, it will be roms[0]
# 
# print("Sonde ID : ", id[0])

# --------------------------------------------------------------------------------
# LPS22HB initialization : atmospheric pressure and temperature inside the payload
# --------------------------------------------------------------------------------

#lps22hb=LPS22HB()
# pressure, temperature = lps22hb.LPS22HB_READ_P_T() # reads once before to remove false values

# --------------------------------------------------------------------------------
# INA219 initialization : battery voltage and current
# --------------------------------------------------------------------------------

bat_mon = ina219.INA219(addr=0x43)

# -----------------------------------------------------------------------------
# Opening and possible creation of data file on the flash - append mode
# First, write a header text for each column
# file will be formated as CSV
# -----------------------------------------------------------------------------
with open(FILENAME, "a") as f:
    f.write("Time;T_out;T_in;pressure;voltage;current\n")

print(f"File '{FILENAME}' initialization on Flash rom")
print(f"Starting measurements: {SAMPLES} samples ({DURATION} sec)...")

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
start_time = time.ticks_ms()
elapsed_time = 0
count = 0

try:
    while count < SAMPLES:
        hb.toggle()
        time.sleep_ms(50)
        hb.toggle()
        
        # Timestamp
        elapsed = time.ticks_diff(time.ticks_ms(), start_time) // 1000

        # call to DS18B20 sensor - must wait a little lesss than 750 ms
        T_out=1.5
#         ds.convert_temp()
#         time.sleep_ms(750)
#         # read outside temperature
#         T_out = ds.read_temp(id[0])
        str_T_out=f"{T_out:.1f}".replace('.',',')
        
        # display for debug
        print(f"[{count}/{SAMPLES}] t={elapsed_time}s | ",
              f"T_out : {str_T_out}°C",end=' | ')
        

        # call to LPS22HB chip (for inside temperature and pressure)
        T_in = 0.1
        pressure = 0.2
        # pressure, temperature = lps22hb.LPS22HB_READ_P_T() # reads once before to remove false values
        str_T_in=f"{T_in:.1f}".replace('.',',')
        str_pressure=f"{pressure:.1f}".replace('.',',')
        # display for debug
        

        # call to ina219 chip (for battery voltage and current)
#         voltage = 0.3
#         current = 0.4
        voltage = bat_mon.getBusVoltage_V()   
        current = bat_mon.getCurrent_mA()   
        str_voltage=f"{voltage:6.3f}".replace('.',',')
        str_current=f"{current:6.3f}".replace('.',',')
        # display for debug
        print(f"V={voltage:6.3f}V | I={current:6.3f}mA")

        # Record data on flash memory
        with open(FILENAME, "a") as f:
            f.write(f"{elapsed_time};{str_T_out};{str_T_in};{str_pressure};{str_voltage};{str_current}\n")

        # wait for the start of a new sampling period
        while (time.ticks_diff(time.ticks_ms(), start_time)<PERIOD):
            pass
        
        start_time = time.ticks_ms()
        elapsed_time=elapsed_time+(PERIOD//1000)
        count = count+1


    print("\n--- end of logging ---")
    print(f"Data saved in '{FILENAME}'.")

except KeyboardInterrupt:
    print("\n program stopped by user.")
    print("\n--- end of logging ---")
    print(f"Data saved in '{FILENAME}'.")