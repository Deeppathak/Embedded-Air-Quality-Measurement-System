# Embedded-Air-Quality-Measurement-System
**Project Description:**

This project centers on designing an embedded system to monitor and report the Air Quality Index (AQI) using sensor data, including PM1.0, PM2.5, PM10.0, temperature, and humidity measurements. These sensors will play a pivotal role in assessing air quality conditions and their potential impact on health and the environment.

**Objective:**
The primary objective of this project is to develop a robust embedded system capable of:

1. Gathering sensor data for PM1.0, PM2.5, PM10.0, temperature, and humidity measurements.
2. Calculating a dynamic AQI value based on the collected sensor data, adhering to recognized standards and algorithms.
3. Transmitting the calculated AQI data to a cloud service for storage, archival, and analysis.
4. Augmenting the AQI calculation with additional local measurements to enhance accuracy and reliability.
5. Reporting the processed AQI data, alongside associated sensor readings, to another cloud service for further analysis and visualization.

**Components:**

1. **Sensor Array:**
   - PM1.0 Sensor: Measures particulate matter with a diameter of 1.0 micrometer or less.
   - PM2.5 Sensor: Measures particulate matter with a diameter of 2.5 micrometers or less.
   - PM10.0 Sensor: Measures particulate matter with a diameter of 10.0 micrometers or less.
   - Temperature Sensor: Monitors ambient temperature conditions.
   - Humidity Sensor: Measures the level of moisture in the air.

2. **Embedded System:**
   - Microcontroller: Processes sensor data and performs real-time calculations.
   - Communication Module: Facilitates data transmission to cloud services.
   - Data Storage: Stores historical sensor readings and calculated AQI values.
   - User Interface: Provides a means for configuration and monitoring of the system.

3. **Cloud Services Integration:**
   - ThingSpeak: Utilized for storing, visualizing, and analyzing sensor data and calculated AQI values.
   - Additional Cloud Service: Employed for advanced data analysis and visualization, catering to specific project requirements.

**Workflow:**

1. **Data Acquisition:**
   - The sensor array continuously gathers PM1.0, PM2.5, PM10.0, temperature, and humidity measurements.

2. **Data Processing:**
   - The embedded system receives sensor data, filters out noise, and computes the AQI value using established algorithms.
   - Additional local measurements are integrated to refine the AQI calculation.

3. **Cloud Integration:**
   - The calculated AQI data is transmitted to ThingSpeak for storage, archival, and visualization.
   - Simultaneously, the processed data is forwarded to another cloud service for in-depth analysis and reporting.

**Expected Outcome:**

The successful implementation of this project will yield an integrated solution for real-time monitoring and reporting of air quality, encompassing various sensor measurements. By leveraging IoT technologies and cloud services, the system will facilitate informed decision-making and interventions to mitigate air pollution and safeguard community well-being.

**Conclusion:**

Our project endeavors to contribute to the ongoing efforts in environmental monitoring and management by developing an innovative embedded system for AQI indication and reporting. Through collaboration with stakeholders and the utilization of cutting-edge technologies, we strive to create a sustainable solution with a tangible impact on air quality assessment and improvement initiatives.
<p align="center"><ins>  Project images </ins></p>

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1yZLoyRm_KqA0Rru7tVPt_xZBcA34tmbn" alt="Image 1" width="500"/>
  <img src="https://drive.google.com/uc?export=view&id=1y-q3IvvfvpQD_X9WKF0srpK_s1XjDYDN" alt="Image 2" width="500"/>
</div>
