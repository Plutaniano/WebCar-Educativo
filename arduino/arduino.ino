// BIBLIOTECAS

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// CONSTS

const char* SSID = "Lucas2"; // rede wifi
const char* PASSWORD = "catarina0701"; // senha da rede wifi

String SERVIDOR = "http://189.62.13.193/";

// DECLARAÇÃO DAS FUNÇÕES

void initSerial();
void initWiFi();
void httpRequest(String path);

// OBJETOS

WiFiClient client;
HTTPClient http;

// CÓDIGO

void setup() {
  Serial.begin(115200);
  initWiFi();
  httpRequest("bind?addr=" + WiFi.localIP().toString() + "&port=5000"); // Declarando ao servidor o IP do arduino
}

void loop() {
}

// FUNÇÕES

void httpRequest(String path) {
  String payload = makeRequest(path);

  if (!payload) {
    return;
  }

  Serial.println("##[RESULT]## ==> " + payload);
}

String makeRequest(String path) {    
  http.begin(SERVIDOR + path);
  int httpCode = http.GET();

  if (httpCode < 0) {
    Serial.println("request error - " + httpCode);
    return "";
  }

  if (httpCode != HTTP_CODE_OK) {
    return "";
  }

  String response =  http.getString();
  http.end();
  return response;
}


void initWiFi() {
  delay(10);
  Serial.println("Conectando-se em: " + String(SSID));

  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado na Rede " + String(SSID) + " | IP => ");
  Serial.println(WiFi.localIP());
}
