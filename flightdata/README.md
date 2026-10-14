
# Flight data analysis.

>[!Note]
>Before performing the data analysis, the relative pressures expressed in the acquisition file were replaced with the absolute pressures as provided by the LPS22HB acquisition circuit (by multiplying them by the inverse of the coefficient used in the initial version of the program). The program `balloon2026_1_2.py` has also been corrected and no longer contains the correction coefficient. <br><br>Subsequently, the acquisition file `balloon_data.csv` was resampled from a 5-second acquisition period to 30 seconds in order to match the files provided by the amateur radio program.

The file with all data and graphics `balloon2026_data_final.xlsx` was created using by LibreOffice Calc and saved on xlsx format. 

>[!Warning]
>As my locale is French, the decimal separator is comma `,`.
>
The flight began at 2:13 PM local time (Brussels) and ended at 5:53 PM, for a total duration of 3 hours and 20 minutes.

## Altitude and vertical speed.

<div align="center">
<img width="498" height="586" alt="up_fig" src="https://github.com/user-attachments/assets/c0c2e9b3-4255-4c45-84b2-c3d013e3fa5e" />
<img width="423" height="563" alt="down_fig" src="https://github.com/user-attachments/assets/68cc086b-a095-45fa-8658-13796b623115" />
</div>div>

The data were extracted from the radio amateur flight files in [amateur.sondehub.org](https://amateur.sondehub.org/#!mt=Mapnik&mz=9&qm=31d&mc=51.2292,5.08887&f=ON7OT-11&q=ON7OT-11). 

<img width="1248" height="869" alt="alt and speed" src="https://github.com/user-attachments/assets/785816a6-6815-4b17-aff1-142ae8ba92b2" />


## Inside & outside payload temperature vs altitude.

<img width="1272" height="849" alt="temp_up" src="https://github.com/user-attachments/assets/43995b71-691b-43db-8957-cc9ad6c17ea9" />

<img width="1153" height="862" alt="temp_down" src="https://github.com/user-attachments/assets/d9f16cf7-08b0-4bcb-8496-fa9cd98d29bc" />


## Pressure data and altitude estimate.

<img width="1249" height="828" alt="alt and pressure" src="https://github.com/user-attachments/assets/11ba9802-2c78-4f8a-9538-6f2cb102b5de" />


## Battery behavior.

<img width="1258" height="844" alt="battery" src="https://github.com/user-attachments/assets/85d097f4-ddbf-4736-8620-8b151fe9953a" />


