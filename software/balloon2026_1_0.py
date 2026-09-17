import machine
from machine import Pin
import onewire
import ds18x20
import time
#import ina219.py
#import lps22hb.py

# -----------------------------------------------------------------------------
# General parameters
# -----------------------------------------------------------------------------
PERIOD = 5000         # sampling rate (in ms)
DURATION = 180   # total acquisition time (in seconds)
FILENAME = "balloon_data.csv"

SAMPLES = DURATION // (PERIOD/1000)

# -----------------------------------------------------------------------------
# Heart beat and status LED
# -----------------------------------------------------------------------------
hb = Pin(25, machine.Pin.OUT)

# -----------------------------------------------------------------------------
# DS18B20 initialization : temperature outside the payload
# -----------------------------------------------------------------------------
PIN_DATA = 22           # DS18B20 on GP22
ow = onewire.OneWire(Pin(PIN_DATA))
ds = ds18x20.DS18X20(ow)

id = ds.scan()  # we have just one sensor, it will be roms[0]

print("Sonde ID : ", id[0])

# --------------------------------------------------------------------------------
# LPS22HB initialization : atmospheric pressure and temperature inside the payload
# --------------------------------------------------------------------------------

#lps22hb=LPS22HB()
# pressure, temperature = lps22hb.LPS22HB_READ_P_T() # reads once before to remove false values

# --------------------------------------------------------------------------------
# INA219 initialization : battery voltage and current
# --------------------------------------------------------------------------------

#ina219 = INA219(addr=0x43)

# -----------------------------------------------------------------------------
# Opening and possible creation of data file on the flash - append mode
# First, write a header text for each column
# file will be formated as CSV
# -----------------------------------------------------------------------------
with open(FILENAME, "a") as f:
    f.write("Time,T_out,T_in,pressure,voltage,current \n")

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
        # Timestamp
        elapsed = time.ticks_diff(time.ticks_ms(), start_time) // 1000

        # call to DS18B20 sensor - must wait a little lesss than 750 ms
        ds.convert_temp()
        time.sleep_ms(750)
        # read outside temperature
        T_out = ds.read_temp(id[0])
        # display for debug
        print(f"[{count}/{SAMPLES}] t={elapsed_time}s | ",
              f"Sonde : {T_out:.1f}°C")
        

        # call to LPS22HB chip (for inside temperature and pressure)
        T_in = 0
        pressure = 0
        # pressure, temperature = lps22hb.LPS22HB_READ_P_T() # reads once before to remove false values
        # display for debug
        

        # call to ina219 chip (for battery voltage and current)
        voltage = 0
        current = 0
        #voltage = ina219.getBusVoltage_V()   
        #current = ina219.getCurrent_mA()   
        # display for debug
        

        # Record data on flash memory
        with open(FILENAME, "a") as f:
            f.write(f"{elapsed_time},{T_out:.1f},{T_in:.1f},{pressure:.1f},{voltage:.1f},{current:.1f}\n")

        # wait for the start of a new sampling period
        while (time.ticks_diff(time.ticks_ms(), start_time)<PERIOD):
            pass
        
        start_time = time.ticks_ms()
        elapsed_time=elapsed_time+(PERIOD//1000)
        count = count+1


    print("\n--- Fin de l'acquisition (30 minutes écoulées) ---")
    print(f"Données enregistrées dans '{FILENAME}'.")

except KeyboardInterrupt:
    print("\nArrêt manuel par l'utilisateur.")