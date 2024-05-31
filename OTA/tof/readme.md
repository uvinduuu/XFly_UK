## OTA Real-Time Data Representation

Beyond firmware updates, OTA communication is also crucial for real-time data representation. The Qubebots XFly drone is equipped with a Time-of-Flight (TOF) sensor (VL53L1X), which provides precise distance measurements. To monitor these readings in real time while the drone is in flight, I implemented the following system:

### Collecting Sensor Data
- The TOF sensor on the drone continuously collects distance measurements. These readings are crucial for applications like obstacle avoidance and altitude maintenance.
  
### Setting Up MQTT Broker
- MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol ideal for IoT applications. I set up an MQTT broker to handle the communication between the drone and the data visualization platform. The ESP32-C3 module publishes the sensor data to the MQTT broker at regular intervals.

### Real-Time Data Visualization with Node-RED
- Node-RED, a powerful flow-based development tool, was used to create a real-time data visualization dashboard. The dashboard subscribes to the MQTT topics and plots the TOF sensor readings on a graph, providing an intuitive and real-time view of the drone’s environment.

## Transition to WiFiManager for Easier WiFi Setup

### Problem
- The manual method of entering SSID and password for WiFi connection was inflexible and cumbersome, especially when deploying the device in various locations with different network configurations. This approach required users to modify the code and re-upload it to the ESP32-C3 whenever the network credentials changed, which is impractical for non-technical users.
  
### Solution
- Integrating the WiFiManager library provided a user-friendly solution. WiFiManager automatically handles the WiFi connection process and offers a web-based interface for selecting and connecting to available WiFi networks. This eliminates the need for hardcoding network credentials and simplifies the setup process, making the device more versatile and easier to deploy in different environments.

*By using WiFiManager, I significantly improved the user experience and flexibility of the Qubebots XFly drone platform, allowing seamless network configuration and enhancing the overall efficiency of the OTA update process.*
