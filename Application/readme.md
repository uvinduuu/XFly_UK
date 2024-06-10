# MQTT and HTTP Uploader Application

This code is a GUI application built with Python's `tkinter` library that interacts with an MQTT broker to receive altitude data and uploads binary files to a specified HTTP server. It visualizes real-time altitude data using `matplotlib`.

## Features

- **MQTT Connection**: Connects to an MQTT broker to subscribe to altitude data.
- **Data Visualization**: Displays real-time altitude data in a line plot.
- **File Upload**: Allows users to upload binary files to a specified HTTP server.

## Dependencies

- `tkinter`: For the GUI.
- `paho-mqtt`: For MQTT communication.
- `requests`: For HTTP file upload.
- `matplotlib`: For plotting the altitude data.
- `threading` and `queue`: For handling MQTT communication in a separate thread.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/qubebots-xfly.git
   cd qubebots-xfly
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install paho-mqtt requests matplotlib
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. The GUI will open, showing the current altitude and a plot of the altitude data over time.

3. Click "Upload Bin File" to upload a binary file to the HTTP server.

## Configuration

- **MQTT Configuration**:
  - `MQTT_BROKER`: The MQTT broker address.
  - `MQTT_PORT`: The MQTT broker port.
  - `MQTT_TOPIC`: The MQTT topic to subscribe to.
  - `MQTT_USER`: The MQTT username.
  - `MQTT_PASSWORD`: The MQTT password.

- **HTTP Server Configuration**:
  - `HTTP_SERVER_URL`: The URL of the HTTP server to upload files to.

## Code Overview

### `MQTTApp` Class

- **`__init__(self, root)`**: Initializes the GUI components, sets up MQTT client, starts MQTT in a separate thread, and initializes data storage for plotting.
- **`start_mqtt(self)`**: Connects to the MQTT broker and starts the MQTT loop.
- **`on_connect(self, client, userdata, flags, rc)`**: Callback for when the client receives a CONNACK response from the server.
- **`on_message(self, client, userdata, msg)`**: Callback for when a PUBLISH message is received from the server.
- **`process_queue(self)`**: Processes messages from the MQTT client.
- **`update_label(self, message)`**: Updates the altitude label with the latest message.
- **`init_plot(self)`**: Initializes the plot for altitude data.
- **`update_plot(self, frame)`**: Updates the plot with new altitude data.
- **`upload_file(self)`**: Opens a file dialog to select a binary file and uploads it to the HTTP server.

