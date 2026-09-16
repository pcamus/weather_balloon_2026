# weather_balloon_2026
This is an [update](https://github.com/pcamus/weather_balloon_project) of weather_balloon_project

In this project I use a Raspberry Pi Pico 2 (powered by a [RP2350](https://www.raspberrypi.com/products/rp2350/) with 4MB of flash memory) and 2 extension modules to design a weather balloon experiment.

The purpose of this experiment is to measure flight parameters of the balloon (pressure, indoor and outdoor temperature).

The programming language is MicroPython.

## Hardware setup.

- A Raspbery Pi Pico.
- A [10-DOF IMU](https://www.waveshare.com/wiki/Pico-10DOF-IMU) from Waveshare.
- A battery module [Pico UPS A](https://www.waveshare.com/wiki/Pico-UPS-A) from Waveshare.

For the prototype I also use a [Quad GPIO Expander](https://www.waveshare.com/pico-quad-expander.htm) from Waveshare

*Prototype setup:*

<img width="1133" height="753" alt="ballon_stack" src="https://github.com/user-attachments/assets/4efe90a2-ebe4-4de1-a8e3-3327e1a03192" />

*The stacked version (wheight = 50 g) looks like that:*
