import time
from machine import I2C

# Adresses I2C courantes
LPS22HB_I2C_ADDR_DEF = 0x5C  # Adresse par défaut (SA0 = 0/GND)
LPS22HB_I2C_ADDR_ALT = 0x5D  # Adresse alternative (SA0 = 1/VCC)

# Registres LPS22HB
WHO_AM_I = 0x0F
CTRL_REG1 = 0x10
CTRL_REG2 = 0x11
PRESS_OUT_XL = 0x28
TEMP_OUT_L = 0x2B

class LPS22HB:
    def __init__(self,address=LPS22HB_I2C_ADDR_DEF):
        self.i2c = I2C(1)
        self.address = address
        
        # Vérification de l'identifiant du capteur (Devrait être 0xB1)
        chip_id = self._read_reg(WHO_AM_I, 1)[0]
        if chip_id != 0xB1:
            raise RuntimeError(f"Capteur LPS22HB non trouvé. ID lu: {hex(chip_id)}")
        
        # Configuration : Mode ODR = 25 Hz, filtre passe-bas activé (CTRL_REG1 = 0x30)
        self._write_reg(CTRL_REG1, 0x30)

    def _read_reg(self, reg, length):
        return self.i2c.readfrom_mem(self.address, reg, length)

    def _write_reg(self, reg, val):
        self.i2c.writeto_mem(self.address, reg, bytes([val]))

    @property
    def pressure(self):
        """Retourne la pression en hPa (hectopascals)"""
        data = self._read_reg(PRESS_OUT_XL, 3)
        # Assemblage des 24 bits (3 octets) de pression
        press_raw = (data[2] << 16) | (data[1] << 8) | data[0]
        # Si le résultat est signé (2's complement)
        if press_raw & 0x800000:
            press_raw -= 0x1000000
        return press_raw / 4096.0

    @property
    def temperature(self):
        """Retourne la température en °C"""
        data = self._read_reg(TEMP_OUT_L, 2)
        # Assemblage des 16 bits (2 octets)
        temp_raw = (data[1] << 8) | data[0]
        if temp_raw & 0x8000:
            temp_raw -= 0x10000
        return temp_raw / 100.0

    @property
    def altitude(self):
        """Calcule une altitude approximative en mètres basée sur le niveau de la mer (1013.25 hPa)"""
        p = self.pressure
        return 44330.0 * (1.0 - (p / 1013.25) ** (1 / 5.255))