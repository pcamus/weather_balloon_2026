# weather_balloon_2026
This is an [update](https://github.com/pcamus/weather_balloon_project) of the 2022 weather_balloon_project.

This updated project uses a Raspberry Pi Pico 2 (powered by a [RP2350](https://www.raspberrypi.com/products/rp2350/) with 4MB of flash memory) and 2 extension modules to design a weather balloon experiment.

The purpose of this experiment is to measure flight parameters of the balloon (pressure, indoor and outdoor temperature, battery voltage and current).


## Hardware setup.

- A Raspbery Pi Pico.
- A [10-DOF IMU](https://www.waveshare.com/wiki/Pico-10DOF-IMU) from Waveshare.
- A battery module [Pico UPS A](https://www.waveshare.com/wiki/Pico-UPS-A) from Waveshare.
- A waterproof version of the [DS18B20](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf) (-55 to 125 °C) in thermoplastic housing

It should be noted that the 10-DOF IMU board used contains two components: an MPU2950 accelerometer and an LPS22HB temperature and humidity sensor circuit.

In this version, we will not be using the accelerometer.

Care must also be taken as the Waveshare 10-DOF IMU board comes in several versions with different, non-compatible chips. The version used here is Version 2.1.
For the prototype I also use a [Quad GPIO Expander](https://www.waveshare.com/pico-quad-expander.htm) from Waveshare

*Prototype setup:*

<img width="1133" height="753" alt="ballon_stack" src="https://github.com/user-attachments/assets/4efe90a2-ebe4-4de1-a8e3-3327e1a03192" />

*The stacked version (wheight = 50 g) looks like that:*

## Software.

The programming language is MicroPython.
