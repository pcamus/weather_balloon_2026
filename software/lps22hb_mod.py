# File : lps22hb_mod.py
# LPS22HB MicroPython class
# Used to access LPS22HB chip on PICO 10DOF IMU
# Chip : https://www.waveshare.com/w/upload/2/20/Lps22hb.pdf
# Pico 10-DOF IMU module : https://www.waveshare.com/wiki/Pico-10DOF-IMU
# info@pcamus.be
# 7/8/2022

from machine import I2C
#i2c address
LPS22HB_I2C_ADDRESS   =  0x5C
#

# LPS22HB used registerr 

ADD_WHO_AM_I   = 0x0F   # Who am I register       
VAL_WHO_AM_I   = 0xB1   # Who am I value

ADD_CTRL_REG1  = 0x10   #Control registers
VAL_CTRL_REG1  = 0x02   #Low-pass filter disabled , output registers not updated
# until MSB and LSB have been read , Enable Block Data Update , Set Output Data Rate to 0   

ADD_CTRL_REG2    = 0x11
SWRESET_MASK     = 0x04   # reset bit mask
ONE_SHOT_MASK    = 0x01   # one shot bit mask

ADD_STATUS       = 0x27   # Status register
P_DA_MASK        = 0x01   # Temperature data available
T_DA_MASK        = 0x02   # Pressure data available

ADD_PRESS_OUT_XL = 0x28   # Pressure output registers (24 bits) LSB first
ADD_PRESS_OUT_L  = 0x29
ADD_PRESS_OUT_H  = 0x2A
ADD_TEMP_OUT_L   = 0x2B   # Temperature output registers (16 bits) LSB first
ADD_TEMP_OUT_H   = 0x2C

class LPS22HB(object):
    def __init__(self,address=LPS22HB_I2C_ADDRESS):
        self._address = address # stores I2C address of LPS22HB
        self._bus = I2C(1) # creates an instance of I2C1 bus 
        self._pressure = 0 # stores pressure measurement
        self._temperature = 0 # stores temperature measurement
                
        # detect if ICM20948 is present
        if self._read_byte(ADD_WHO_AM_I)==VAL_WHO_AM_I:
            print("LPS22HB detected.\r\n")
        else :
            print("No LPS22HB detected - exiting program.")
            sys.exit()
            
        self.LPS22HB_RESET()  # Reset LPS22HB
        
    def LPS22HB_RESET(self):
        Buf = self._read_byte(ADD_CTRL_REG2)
        Buf = Buf | SWRESET_MASK                                         
        self._write_byte(ADD_CTRL_REG2,Buf)   #SWRESET bit Set to 1
        while Buf: #SWRESET bit is clear when reset is completed
            Buf = self._read_byte(ADD_CTRL_REG2)
            Buf = Buf & SWRESET_MASK
    
    def LPS22HB_READ_P_T(self):
    
        self.LPS22HB_START_ONESHOT()
        
        if (self._read_byte(ADD_STATUS) & P_DA_MASK):  # a new pressure data is generated
            data = self._read_block(ADD_PRESS_OUT_XL,3)
            self._pressure=((data[2]<<16)+(data[1]<<8)+data[0])/4096.0
                
        if (self._read_byte(ADD_STATUS) & T_DA_MASK):   # a new pressure data is generated
            data=self._read_block(ADD_TEMP_OUT_L,2)
            self._temperature=((data[1]<<8)+data[0])/100.0
            
            return self._pressure, self._temperature
    
    def LPS22HB_START_ONESHOT(self):
        Buf = self._read_byte(ADD_CTRL_REG2)
        Buf = Buf | ONE_SHOT_MASK      # Start new acquisition
        self._write_byte(ADD_CTRL_REG2,Buf)
   
    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
       
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
