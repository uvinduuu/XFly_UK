#define MDASH_APP_NAME "MinimalApp"
#include <mDash.h>

#include <WiFi.h>

#define WIFI_NETWORK "SSID"
#define WIFI_PASSWORD "Password"
#define DEVICE_PASSWORD "ID_from_mDash"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  motor_setup();
  Serial.begin(115200);
  WiFi.begin(WIFI_NETWORK, WIFI_PASSWORD);
  mDashBegin(DEVICE_PASSWORD);
}

void loop() {
  // put your main code here, to run repeatedly:
}
