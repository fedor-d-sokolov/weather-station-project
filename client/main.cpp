#include <Wire.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <DFRobot_BMP280.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

typedef DFRobot_BMP280_IIC    BMP;
BMP   bmp(&Wire, BMP::eSdoLow);

#define DHTTYPE    DHT22

DHT_Unified dht(D3, DHTTYPE);

HTTPClient http;
WiFiClient httpClient;

/*
 * Сервер,
 * IP: 77.223.98.108:
 * Порт: 1337
*/
String serverName = "http://77.223.98.108:1337/webhook";

// Пространство имен на будущее чтобы не было ошибок компиляции
namespace bmp_custom
{
  float temperature = 1.0f;
  float pressure = 1.0f;
};

void setup()
{
  // Для работы консоли
  Serial.begin(115200); 

  // Переключаем режим пина на вывод
  pinMode(D3, INPUT);

  // Подключаемся к Wi-Fi
  WiFi.begin("DLI-TL20", "donteventry");

  dht.begin();
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  
  bmp.reset();
  Serial.println("Setuping BMP280...");
  while(bmp.begin() != BMP::eStatusOK) {
    Serial.println("BMP280 initialization failed.");
    delay(2000);
  }
  
  // Ждем пока не подключимся
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Waiting for WiFi connection.");
    delay(1000);
  }
  
}

void loop()
{
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  
  int dht_temperature = event.temperature;

  dht.humidity().getEvent(&event);
  int dht_humidity = event.relative_humidity;
  
  // Добавляем в параметры температуру и влажность от DHT22
  String serverPath = serverName + String("?dht_22_temperature=") + String(dht_temperature) + String("&dht_22_humidity=") + String(dht_humidity) + String("&bmp_280_temperature=") + String(bmp.getTemperature()) + String("&bmp_280_pressure=") + String(bmp.getPressure()) + String("&light=") + String("light");

  // Начинаем отсылать запрос, serverPath.c_str() --> перевод строки в неизменяемую
  http.begin(httpClient, serverPath.c_str());

  // Отсылаем запрос и получаем HTTPcode (https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_HTTP)
  int httpResponseCode = http.GET();

  
  delay(15000);
}
