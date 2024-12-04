#include <DHT.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
#include "Adafruit_BMP085.h"

DHT dht(2, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);
RTC_DS1307 rtc;
Adafruit_BMP085 bmp;

float hum, temp;
int h, m, s, pres;

void setup() {
  dht.begin();
  rtc.begin();
  bmp.begin();
  lcd.init();
  lcd.backlight();
}

void loop() {
  hum  =  dht.readHumidity();
  temp = dht.readTemperature();
  pres = bmp.readPressure();

  // К большому сожалению, я не смог найти онлайн симулятора, поддерживающего BMP180

  DateTime now = rtc.now();
  h = now.hour();
  m = now.minute();
  s = now.second();

  lcd.setCursor(0, 0);
  lcd.print(h);
  lcd.print(":");
  lcd.print(m);
  lcd.print(":");
  lcd.print(s);
  lcd.print(" ");
  lcd.print(temp);
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.print(pres);
  lcd.print("PA ");
  lcd.print(hum);
  lcd.print("%");

  delay(1000);
}

