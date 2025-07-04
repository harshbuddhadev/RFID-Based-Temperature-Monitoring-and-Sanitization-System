# RFID based Temperature Monitoring and Sanitization System

## Project Overview
RFID-Based Temperature Monitoring and Sanitization System is a Raspberry Pi–driven kiosk designed for contactless health screening and hygiene enforcement. By scanning an RFID-enabled ID card, the system:

1. Identifies the user via RFID.
2. Measures body temperature with a connected sensor.
3. Displays the temperature reading in real time.
4. Optionally dispenses hand sanitizer automatically after temperature is taken.

Originally built between December 2021 and April 2022, this project combines temperature monitoring and sanitizer dispensing with attendance logging functionality 

## Key Features
- RFID identification: detects and logs individual users via RFID tags
- Temperature screening: non-invasive measurement using a digital sensor
- Hygienic response: enables automatic sanitizer release post-temperature check
- Attendance tracking: logs user presence along with timestamped health data
- Modular architecture: structured Python code for easy customization and extension

## Components & Technologies
- Hardware:
    - Raspberry Pi (control unit)
    - RFID reader with compatible tags
    - Temperature sensor (e.g., DS18B20 or similar)
    - Sanitizer dispenser module (pump or actuator)

- Software:
    - Python scripts coordinating RFID reads, temperature checks, display output, and sanitizer activation
    - Optional data logging to CSV or database for tracking

# System Workflow
1. User presents RFID tag to the reader.
2. System reads the tag UID and looks up user ID.
3. Temperature sensor takes a measurement.
4. Temperature result is displayed on screen or console.
5. If enabled, sanitizer dispenser activates.
6. All data (user ID, temperature, timestamp) is logged for reporting.

## Use Cases
Ideal for deployment in environments requiring scalable health safety measures, such as:

- Offices or coworking spaces (for daily health checks and attendance logs)
- Educational institutions (schools, colleges)
- Clinics, labs, or public-entry points

## Getting Started
1. Assemble hardware components following your wiring diagram (RFID reader, sensor, pump).
2. Install required Python libraries (RFID, GPIO, sensor-specific drivers).
3. Configure user data mapping for RFID tag IDs.
4. Edit settings (e.g., sanitizer activation toggle, log file paths).
5. Run the main script to initiate the kiosk workflow.