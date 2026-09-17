# weather_balloon_2026
This is an update of the [2022 weather_balloon_project](https://github.com/pcamus/weather_balloon_project).

Since the update was requested on very short notice, we built upon the previous version, replacing the processor board with its newer version offering more flash memory.

Due to a lack of time for fine-tuning, we removed the acceleration measurement feature, which had not yielded the expected results because of an too low sampling rate. The objective of these measurements was to compare the balloon's behavior during its liftoff phase against a theoretical model.

To maintain interest in the planned flight, however, we added other measurements that were easy to implement: temperature outside the payload box and battery performance throughout the flight.

So, in summary, our system will measure: the temperature inside and outside the payload box, atmospheric pressure, battery voltage, and the current supplied by the battery. Measurements will be taken every 5 seconds.

The balloon's position over time should be provided by amateur radio operators who will track the balloon (using their own radio module, also carried onboard the payload box). They will also recover our system upon landing (conditions permitting) in order to retrieve the flight data stored in our module.

## Hardware setup.

- A Raspbery Pi Pico 2 (powered by a [RP2350](https://www.raspberrypi.com/products/rp2350/) with 4MB of flash memory).
- A [10-DOF IMU](https://www.waveshare.com/wiki/Pico-10DOF-IMU) from Waveshare.
- A battery module [Pico UPS A](https://www.waveshare.com/wiki/Pico-UPS-A) from Waveshare.
- A waterproof version of the [DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) (-55 to 125 °C) in thermoplastic housing

It should be noted that the 10-DOF IMU board used contains two components: an MPU2950 accelerometer and an LPS22HB temperature and humidity sensor circuit.

In this version, we will not be using the accelerometer.

Care must also be taken as the Waveshare 10-DOF IMU board comes in several versions with different, non-compatible chips. The version used here is Version 2.1.

For the prototype I also use a [Quad GPIO Expander](https://www.waveshare.com/pico-quad-expander.htm) from Waveshare

*The stacked version (wheight = 50 g) looks like that(DS18B20 sensor not shown):*

<img width="1133" height="753" alt="ballon_stack" src="https://github.com/user-attachments/assets/4efe90a2-ebe4-4de1-a8e3-3327e1a03192" />



## Software.

The programming language is MicroPython.
