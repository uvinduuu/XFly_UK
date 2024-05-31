#include <WiFi.h>
#include <PubSubClient.h>
#include "Adafruit_VL53L1X.h"
#include <WiFiManager.h>

// WiFi credentials
/*
const char* ssid = "SSID";
const char* password = "Password";
*/

// MQTT broker details
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_user = "XFly";
const char* mqtt_password = "qubebots";

// VL53L1X sensor pins
#define IRQ_PIN 2
#define XSHUT_PIN 3

Adafruit_VL53L1X vl53 = Adafruit_VL53L1X(XSHUT_PIN, IRQ_PIN);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long previousMillis = 0;
const unsigned long interval = 1000; // 1 second

void setup() {
  Serial.begin(115200);

  while (!Serial) delay(10);

  setupTOFSensor();
  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (vl53.dataReady()) {
      int distance = vl53.distance();
      if (distance == -1) {
        // Something went wrong!
        Serial.print(F("Couldn't get distance: "));
        Serial.println(vl53.vl_status);
      } else {
        Serial.print(F("Distance: "));
        Serial.print(distance);
        Serial.println(F(" mm"));

        // Publish distance to MQTT
        char msg[50];
        snprintf(msg, 50, "Distance: %d mm", distance);
        mqttClient.publish("sensorDistance_XFlyUK", msg);
      }
    }
  }
}

void setup_wifi() {
  /*
  //Manual method
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}*/

  //Wifi Manager
  while (!Serial) delay(10); // Wait for Serial Monitor to open

  WiFiManager wifiManager;

  bool connected = wifiManager.autoConnect("Uvindu's XFly", "123456");

  if (!connected) {
    Serial.println("Failed to connect to WiFi");
    ESP.restart(); // Restart ESP32
  } else {
    Serial.println("Connected to WiFi");
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setupTOFSensor() {
  Serial.println(F("Adafruit VL53L1X sensor demo"));

  Wire.begin();
  if (!vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("VL53L1X sensor OK!"));

  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1) delay(10);
  }
  Serial.println(F("Ranging started"));

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());
}
