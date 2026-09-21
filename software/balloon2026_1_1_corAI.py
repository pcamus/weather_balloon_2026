# File : balloon2026_1_1_fixed.py
import machine
from machine import Pin
import onewire
import ds18x20
import time
import ina219
import lps22hb
import os

# -----------------------------------------------------------------------------
# Paramètres généraux
# -----------------------------------------------------------------------------
PERIOD = 5000         # Intervalle d'échantillonnage (ms)
DURATION = 180        # Durée totale d'acquisition (s)
FILENAME = "balloon_data.csv"
CORR_PRESS = 1033 / 991  # Correction barométrique

SAMPLES = DURATION // (PERIOD // 1000)

# -----------------------------------------------------------------------------
# LED Témoin / Heartbeat
# -----------------------------------------------------------------------------
hb = Pin(25, Pin.OUT)
hb.off()

# -----------------------------------------------------------------------------
# Initialisation DS18B20 (Température extérieure)
# -----------------------------------------------------------------------------
PIN_DATA = 22
ow = onewire.OneWire(Pin(PIN_DATA))
ds = ds18x20.DS18X20(ow)

ds_roms = ds.scan()
if not ds_roms:
    print("ATTENTION : Aucun capteur DS18B20 détecté !")
else:
    print(f"DS18B20 détecté ID : {''.join(f'{b:02x}' for b in ds_roms[0])}")

# -----------------------------------------------------------------------------
# Initialisation LPS22HB & INA219
# -----------------------------------------------------------------------------
lps = lps22hb.LPS22HB()
bat_mon = ina219.INA219(addr=0x43)

# Signal sonore/visuel : 2 clignotements = initialisation OK
for _ in range(2):
    hb.on()
    time.sleep_ms(500)
    hb.off()
    time.sleep_ms(500)

# -----------------------------------------------------------------------------
# Initialisation du fichier CSV (Ecriture de l'en-tête uniquement si nouveau)
# -----------------------------------------------------------------------------
file_exists = True
try:
    os.stat(FILENAME)
except OSError:
    file_exists = False

if not file_exists:
    with open(FILENAME, "w") as f:
        f.write("Time;T_out;T_in;pressure;voltage;current\n")

# -----------------------------------------------------------------------------
# Boucle principale d'acquisition
# -----------------------------------------------------------------------------
start_mission_time = time.ticks_ms()
count = 0

while count < SAMPLES:
    cycle_start = time.ticks_ms()
    
    # LED Flash rapide (Heartbeat)
    hb.on()
    time.sleep_ms(50)
    hb.off()
    
    # Temps écoulé depuis le début de la mission (en secondes)
    elapsed_time = time.ticks_diff(cycle_start, start_mission_time) // 1000

    # 1. Lecture DS18B20
    str_T_out = "NC"
    if ds_roms:
        try:
            ds.convert_temp()
            time.sleep_ms(750)  # Attente de conversion 12-bit
            T_out = ds.read_temp(ds_roms[0])
            str_T_out = f"{T_out:.1f}".replace('.', ',')
        except Exception as e:
            print(f"Erreur DS18B20: {e}")

    # 2. Lecture LPS22HB
    try:
        pressure = lps.pressure * CORR_PRESS
        T_in = lps.temperature
        str_T_in = f"{T_in:.1f}".replace('.', ',')
        str_pressure = f"{pressure:.1f}".replace('.', ',')
    except Exception as e:
        str_T_in, str_pressure = "NC", "NC"
        print(f"Erreur LPS22HB: {e}")

    # 3. Lecture INA219
    try:
        voltage = bat_mon.getBusVoltage_V()
        current = bat_mon.getCurrent_mA()
        str_voltage = f"{voltage:.3f}".replace('.', ',')
        str_current = f"{current:.3f}".replace('.', ',')
    except Exception as e:
        str_voltage, str_current = "NC", "NC"
        print(f"Erreur INA219: {e}")

    # 4. Enregistrement sécurisé dans la Flash
    try:
        with open(FILENAME, "a") as f:
            f.write(f"{elapsed_time};{str_T_out};{str_T_in};{str_pressure};{str_voltage};{str_current}\n")
    except OSError as e:
        print(f"Erreur écriture Flash: {e}")

    count += 1

    # 5. Calcul du temps de pause restant (pour maintenir un rythme exact de 5s sans dérive)
    elapsed_in_cycle = time.ticks_diff(time.ticks_ms(), cycle_start)
    remaining_sleep = PERIOD - elapsed_in_cycle
    
    if remaining_sleep > 0:
        time.sleep_ms(remaining_sleep)

# Signal de fin (LED allumée 2 secondes)
hb.on()
time.sleep_ms(2000)
hb.off()
print("Acquisition terminée avec succès.")