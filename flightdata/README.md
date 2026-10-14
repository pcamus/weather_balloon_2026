
# Flight data analysis.

>[!Note]
>Before performing the data analysis, the relative pressures expressed in the acquisition file were replaced with the absolute pressures as provided by the LPS22HB acquisition circuit (by multiplying them by the inverse of the coefficient used in the initial version of the program). The program `balloon2026_1_2.py` has also been corrected and no longer contains the correction coefficient. <br><br>Subsequently, the acquisition file `balloon_data.csv` was resampled from a 5-second acquisition period to 30 seconds in order to match the files provided by the amateur radio program.

The file with all data and graphics `balloon2026_data_final.xlsx` was created using by LibreOffice Calc and saved on xlsx format. 

>[!Warning]
>As my locale is French, the decimal separator is comma `,`.
>
The flight began at 2:13 PM local time (Brussels) and ended at 5:53 PM, for a total duration of 3 hours and 20 minutes.

## Equations of motion.
<table>
  <tr>
    <td width="30%">
      <img width="428" height="563" alt="up_fig" src="https://github.com/user-attachments/assets/52fd6122-1847-44b4-b27b-01beb1f55407" /> 
    </td>
    <td>
      <h3>Equation of motion for the balloon's ascent.</h3>
      <p></p>
      <p>Three forces are at play:      
        
- **Buoyancy** (Archimedes' force): $B = \rho_{\text{air}} \cdot V_{\text{balloon}} \cdot g$
- **Weight** (of the balloon and payload): $W = (m_{\text{balloon}} + m_{\text{payload}}) \cdot g$
- **Drag force**: $D = \frac{1}{2} \cdot C_x \cdot \rho_{\text{air}} \cdot S \cdot v^2$
  </p>
  <p>Due to Newton's second law: $m \cdot a = m \cdot \frac{dv}{dt} = \sum \vec{F}_i$
    and taking into account the signs of the forces, this leads to:</p>
    <p> 
    $$m \cdot \frac{dv}{dt} = \rho_{\text{air}} \cdot V_{\text{balloon}} \cdot g - (m_{\text{balloon}} + m_{\text{payload}}) \cdot g - \frac{1}{2} \cdot C_x \cdot \rho_{\text{air}} \cdot S \cdot v^2$$
    </p>

  <p> $S$ is the cross section of the ballon, $v$ the ascent velocity and $C_x$ the aerodynamic coefficient</p>
  <p>Velocity is positive upwards.</p>
    </td>
  </tr>
</table>

<table>
  <tr>
    <td width="30%">
      <img width="423" height="563" alt="down_fig" src="https://github.com/user-attachments/assets/0ef28b12-4326-4858-bbee-03b73f8cd3eb" /> 
    </td>
    <td>
      <h3>Equation of motion for the balloon's descent</h3>
      <p></p>
      <p>Three forces are at play:      
        
- **Weight** (of the balloon and payload): $W = (m_{\text{balloon vide}} + m_{\text{payload}}) \cdot g$
- **Drag force**: $D = \frac{1}{2} \cdot C_x \cdot \rho_{\text{air}} \cdot S \cdot v^2$
  </p>
  <p>Due to Newton's second law: $m \cdot a = m \cdot \frac{dv}{dt} = \sum \vec{F}_i$
    and taking into account the signs of the forces, this leads to:</p>
    <p>   
      $$m \cdot \frac{dv}{dt} = \frac{1}{2} \cdot C_x \cdot \rho_{\text{air}} \cdot S \cdot v^2 - (m_{\text{balloon vide}} + m_{\text{payload}}) \cdot g$$
    </p>
  </p>
  <p> $S$ is the cross section of the ballon, $v$ the ascent velocity and $C_x$ the aerodynamic coefficient</p>
  <p>Velocity is positive upwards.</p>
    </td>
  </tr>
</table>

## Altitude and vertical speed.


The data were extracted from the radio amateur flight files in [amateur.sondehub.org](https://amateur.sondehub.org/#!mt=Mapnik&mz=9&qm=31d&mc=51.2292,5.08887&f=ON7OT-11&q=ON7OT-11). 

<img width="1248" height="869" alt="alt and speed" src="https://github.com/user-attachments/assets/785816a6-6815-4b17-aff1-142ae8ba92b2" />

<p>
The average measured ascent velocity over the first 1,000 m is <b>4m/s</b>, and the descent velocity is <b>3.3 m/s</b>.Theoretical calculations for a 48-inch balloon with a 250 g payload, an ascent Cx of 0.3, a descent Cx of 0.75, and a parachute surface area of 0.79 m² give <b>4.2 m/s</b> for the ascent and <b>2.8 m/s</b> for the descent.
</p>
<p>
To perform the theoretical calculation, we assume terminal velocity by setting the acceleration term to zero ($\frac{dv}{dt} = 0$). 
</p>
<br>

## Inside & outside payload temperature vs altitude.

<img width="1272" height="849" alt="temp_up" src="https://github.com/user-attachments/assets/43995b71-691b-43db-8957-cc9ad6c17ea9" />

<img width="1153" height="862" alt="temp_down" src="https://github.com/user-attachments/assets/d9f16cf7-08b0-4bcb-8496-fa9cd98d29bc" />


## Pressure data and altitude estimate.

<img width="1249" height="828" alt="alt and pressure" src="https://github.com/user-attachments/assets/11ba9802-2c78-4f8a-9538-6f2cb102b5de" />


## Battery behavior.

<img width="1258" height="844" alt="battery" src="https://github.com/user-attachments/assets/85d097f4-ddbf-4736-8620-8b151fe9953a" />


