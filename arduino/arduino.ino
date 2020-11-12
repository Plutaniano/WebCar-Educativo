// BIBLIOTECAS
#include <Arduino.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// CONSTS

const char* SSID = "NOME-DA-REDE"; // rede wifi
const char* PASSWORD = "SENHA-DA-REDE"; // senha da rede wifi

const String SERVIDOR = "http://carrara.taxi";
const int PORT = 80;

// OBJETOS

ESP8266WebServer server(PORT);

// PINS

int led = LED_BUILTIN;

// Endpoints

void handleRoot()
{
  server.send(200, "text/plain", "Servidor ligado");
}
void handleNotFound() 
{
  String message = "404";
  server.send(404, "text/plain", message);
}
void ledOn()
{

}
void ledOff() 
{

}
void ledToggle()
{
  int status = digitalRead(led);
  digitalWrite(led, !status);
  server.send(200, "text/plain", String(!status));
}
void buzzer()
{

}

// Funções auxiliares

void wifi_init()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConectado a");
  Serial.println(SSID);
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266"))
  {
    Serial.println("DNS OK!");
  }
}
void HTTP_request()
{
  WiFiClient client;
  HTTPClient http;

  if (http.begin(client, SERVIDOR + "/conectar?addr=" + WiFi.localIP().toString().c_str() + "&port=" + PORT))
  {
    int httpStatus = http.GET();
    Serial.println("HTTP GET CODE" + httpStatus);
    
    if (httpStatus > 0)
    {
      if (httpStatus == HTTP_CODE_OK || httpStatus == HTTP_CODE_MOVED_PERMANENTLY)
      {
        String payload = http.getString();
        Serial.println(payload);
      } else {
        Serial.printf("ERRO HTTP %s\n", http.errorToString(httpStatus).c_str());
      }

      http.end();
    }
  } else {
    Serial.printf("HTTP Sem conexão\n");
  }
}

// MAIN

void setup()
{
  Serial.begin(115200);
  Serial.println("booting");
  pinMode(led, OUTPUT);
  
  wifi_init();

  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  
  server.on("/ledon", ledOn);
  server.on("/ledoff", ledOff);
  server.on("/ledtoggle", ledToggle);
  server.on("/buzzer", buzzer);

  server.begin();
  HTTP_request();
}

void loop()
{
  server.handleClient();
  MDNS.update();
}
