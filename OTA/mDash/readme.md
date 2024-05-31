## Limitations

While this custom OTA solution was functional, it had several limitations:

- Same Network Requirement: *The drone and the computer used to upload the firmware had to be on the same WiFi network. This limited the flexibility and convenience of performing OTA updates remotely.*
- Scalability Issues: *Managing and updating multiple devices individually with this setup was cumbersome and inefficient.*

## OTA Firmware Update using mDash

To streamline the firmware update process, I built a robust platform using mDash. mDash is a comprehensive device management solution that facilitates secure and efficient OTA updates. Here’s a brief overview of the steps involved:

### Setting Up mDash
- I created an account on the mDash platform and registered the ESP32-C3 device. This process involved generating device-specific credentials to ensure secure communication between the device and the mDash server.

### Preparing the Firmware
- The next step was to compile the firmware and generate the binary (.bin) file. This file contains the updated code that needs to be flashed onto the drone.

### Uploading the Firmware
- Using mDash, I uploaded the .bin file to the platform. mDash handles the distribution of the firmware to the registered devices, ensuring that each device receives the update securely and efficiently.

### Executing the Update
- The ESP32-C3 module on the drone periodically checks for updates on the mDash server. Once an update is detected, the device downloads and installs the new firmware autonomously. This process eliminates the need for manual intervention, making firmware updates seamless and hassle-free.
