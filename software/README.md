# Python code for weather_balloon_2026

The software is written in Micropython for a Raspberry pi pico

balloon2026_x_y.py is the main file.
The code needs 3 modules for the sensors :
- ds18x20.py for the DS18B20 outdoors temperatutre sensor. This module is part of the MicroPython distribution.
- ina219.py for the battery monitoring
- lps22hb_mod.py for the inside temperature and the atmospheric pressure.
