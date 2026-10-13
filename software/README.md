# Python code for weather_balloon_2026

The software is written in Micropython for a Raspberry pi pico

balloon2026_1_0.py is the main file.
The code needs 3 modules for the sensors :
- ds18x20.py for the DS18B20 outdoors temperatutre sensor. This module is part of the MicroPython distribution.
- ina219.py for the battery monitoring
- lps22hb_mod.py for the inside temperature and the atmospheric pressure.

Results are stored in a csv file : balloon_data.csv

The power consumption of the module was measured and is on the order of 120 mW. My 3.7V (type 14500) batteries has a capacity of 2.96Wh.
This provides a theoretical autonomy of 24 h 40 min.


A file size estimate is 46 kb for an hour.

balloon2026_1_1.py is the next main file. I uses another module for the lps22hb : lps22hb.py

After testing the code with success, I asked Gemini AI to show me some weaknesses and to correct the code

The AI corrected code is balloon2026_1_1_corAI.py and the corrections are explained in [Code_Review_Report_Balloon2026.pdf](Code_Review_Report_Balloon2026.pdf)

The AI was in its turn corrected (wrong object name for lps22hb and useless print to report errors - an improvement will be to add a error log file).
Current stable version is [balloon2026_1_2.py](balloon2026_1_2.py). 

The code was tested during a 6 hours run. Real file size was 154 kb.
 
After the flight, it appears that absolute pressure has to be used instead of relative pressure. 
The code contains a pressure coefficient (CORR_PRESS = 1033 / 991) to convert from absolute to relative (to sea level) pressure which was removed  in the last update of the software. The balloon_data.csv contains relative pressure.
