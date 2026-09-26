# Python code for weather_balloon_2026

The software is written in Micropython for a Raspberry pi pico

balloon2026_1_0.py is the main file.
The code needs 3 modules for the sensors :
- ds18x20.py for the DS18B20 outdoors temperatutre sensor. This module is part of the MicroPython distribution.
- ina219.py for the battery monitoring
- lps22hb_mod.py for the inside temperature and the atmospheric pressure.

Results are stored in a csv file : balloon_data.csv

The power consumption of the module was measured and is on the order of 140 mWh for an hour. My 3.6V 14450 batteries have a capacity of 3Wh
A file size estimate is 46 kb for an hour.

balloon2026_1_1.py is the next main file. I uses another module for the lps22hb : lps22hb.py

After testing the code with success, I asked Gemini AI to show me some weaknesses and to correct the code

The AI corrected code is balloon2026_1_1_corAI.py and the corrections are explained in [Code_Review_Report_Balloon2026.pdf](Code_Review_Report_Balloon2026.pdf)

The AI was in its turn corrected (wrong object name for lps22hb and useless print to report errors - an improvement will be to add a error log file).
Current stable version is [balloon2026_1_2.py](balloon2026_1_2.py). 

The code was tested during a 6 hours run. Real file size was 154 kb.
