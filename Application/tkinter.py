import tkinter as tk
from tkinter import filedialog, messagebox
import paho.mqtt.client as mqtt
import requests
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import queue

# MQTT Configuration
MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'sensorDistance_XFlyUK'
MQTT_USER = 'XFly'
MQTT_PASSWORD = 'qubebots'

# HTTP Server Configuration
HTTP_SERVER_URL = 'http://example.com/upload'

class MQTTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Qubebots - XFly")
        
        self.label = tk.Label(root, text="Current Altitude: ", font=("Helvetica", 14))
        self.label.pack(pady=20)
        
        self.message_display = tk.Label(root, text="", font=("Helvetica", 25))
        self.message_display.pack(pady=20)
        
        self.upload_button = tk.Button(root, text="Upload Bin File", command=self.upload_file)
        self.upload_button.pack(pady=20)
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # Start MQTT in a separate thread
        self.mqtt_thread = threading.Thread(target=self.start_mqtt)
        self.mqtt_thread.daemon = True
        self.mqtt_thread.start()
        
        # Initialize data storage for plotting
        self.distances = deque(maxlen=60)  # Store the last 60 values (20 seconds * 3)
        
        # Queue for safely passing messages between threads
        self.message_queue = queue.Queue()

        # Periodically check the message queue
        self.root.after(100, self.process_queue)
        
        # Set up Matplotlib figure and axis in a non-blocking way
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-', label='Altitude (mm)')
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, 3000)  # Adjust based on your sensor's range
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Altitude (mm)')
        self.ax.set_title('Altitude Over Time')
        self.ax.legend()

        # Use Tkinter's `FigureCanvasTkAgg` to integrate Matplotlib with Tkinter
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, init_func=self.init_plot, interval=1000, blit=True, cache_frame_data=False)
        self.canvas.draw()

    def start_mqtt(self):
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.mqtt_client.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(MQTT_TOPIC)
        
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        print(f"Received message: {message}")
        self.message_queue.put(message)
    
    def process_queue(self):
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.update_label(message)
                try:
                    distance = int(message.split(":")[1].strip().split()[0])
                    self.distances.append(distance)
                except Exception as e:
                    print(f"Failed to parse message: {e}")
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)
    
    def update_label(self, message):
        self.message_display.config(text=message)
    
    def init_plot(self):
        self.line.set_data([], [])
        return self.line,
    
    def update_plot(self, frame):
        self.line.set_data(range(len(self.distances)), list(self.distances))
        self.canvas.draw()
        return self.line,
        
    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    response = requests.post(HTTP_SERVER_URL, files={'file': f})
                if response.status_code == 200:
                    messagebox.showinfo("Success", "File uploaded successfully!")
                else:
                    messagebox.showerror("Error", f"Failed to upload file. Status code: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MQTTApp(root)
    root.mainloop()
