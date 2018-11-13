#include <SoftwareSerial.h>
#include <LedControl.h>
#include <Wire.h>
#include "Adafruit_GFX.h"
#include "Adafruit_LEDBackpack.h"

#define LED_RED 1
#define LED_YELLOW 2
#define LED_GREEN 3
SoftwareSerial BTSerial(2,3); // SoftwareSerial(TX, RX)
byte buffer[1024]; // 데이터를 수신 받을 버퍼
int bufferPosition; // 버퍼에 데이타를 저장할 때 기록할 위치
int A = 0x11;
int led_set =0;
int vibr_Pin = A0;
int cnt = 1;
int i = 0;
long measurement;
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();


void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  Serial.println("8x8 LED Matrix Test");
  bufferPosition = 0; // 버퍼 위치 초기화
  matrix.begin(0x70);  // pass in the address
  matrix.clear();
  matrix.blinkRate(1);
  matrix.setRotation(3);
  //matrix.writeDisplay();
  matrix.drawPixel(4, 2, 1);matrix.writeDisplay();
  matrix.setBrightness(15);  

  matrix.drawPixel(0, 0, led_set);matrix.writeDisplay();
}


static const uint8_t PROGMEM
  love_bmp[]=
  {(0,0,0x00),
   (0,1,0x66),
   (0,2,0xff),
   (0,3,0xff),
   (0,4,0x7e),
   (0,5,0x3c),
   (0,6,0x18),
   (0,7,0x00),},
  smile_bmp[] =
  { B00111100,
    B01000010,
    
    B10100101,
    B10000001,
    B10100101,
    B10011001,
    B01000010,
    B00111100 },
  neutral_bmp[] =
  { B00111100,
    B01000010,
    B10100101,
    B10000001,
    B10111101,
    B10000001,
    B01000010,
    B00111100 },
  frown_bmp[] =
  { B00111100,
    B01000010,
    B10100101,
    B10000001,
    B10011001,
    B10100101,
    B01000010,
    B00111100 },
  cross_bmp[]=
  {B10000001,
   B01000010,
   B00100100,
   B00011000,
   B00011000,
   B00100100,
   B01000010,
   B10000001,
   },
  crossBig_bmp[]=
   {B11000011,
    B11100111,
    B01111110,
    B00111100,
    B00111100,
    B01111110,
    B11100111,
    B11000011,},
  reset_bmp[]=
  {B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000,
  B00000000
  };
 
void loop() {
//충격값 확장
measurement=pulseIn (vibr_Pin, HIGH);


if(BTSerial.available()){
  if(Serial.available()){
    BTSerial.write(Serial.read());
  }

switch(BTSerial.read()) 
{
  Serial.write(BTSerial.read());
  case '+':  // led 제어 시작
  
  while(cnt)
  {
    switch(BTSerial.read()) 
    {
    Serial.write(BTSerial.read());
    case '!':
      led_set = 1;
      break;
    case '@':
      led_set = 2;
      break;
    case '#':
  led_set = 3;
  break;
  case '$':
  led_set = 0;
  break;
  
  case 'A':
  matrix.drawPixel(0, 0, led_set);matrix.writeDisplay();
  break;
  case 'B':
  matrix.drawPixel(1, 0, led_set);matrix.writeDisplay();
  break;
  case 'C':
  matrix.drawPixel(2, 0, led_set);matrix.writeDisplay();
  break;
  case 'D':
  matrix.drawPixel(3, 0, led_set);matrix.writeDisplay();
  break;
  case 'E':
   
  matrix.drawPixel(4, 0, led_set);matrix.writeDisplay();
  break;
  case 'F':
   
  matrix.drawPixel(5, 0, led_set);matrix.writeDisplay();
  break;
  case 'G':
   
  matrix.drawPixel(6, 0, led_set);matrix.writeDisplay();
  break;
  case 'H':
   
  matrix.drawPixel(7, 0, led_set);matrix.writeDisplay();
  break;
  case 'I':
   
  matrix.drawPixel(0, 1, led_set);matrix.writeDisplay();
  break;
  case 'J':
   
  matrix.drawPixel(1, 1, led_set);matrix.writeDisplay();
  break;
  case 'K':
   
  matrix.drawPixel(2, 1, led_set);matrix.writeDisplay();
  break;
  case 'L':
   
  matrix.drawPixel(3, 1, led_set);matrix.writeDisplay();
  break;
  case 'M':
   
  matrix.drawPixel(4, 1, led_set);matrix.writeDisplay();
  break;
  case 'N':
   
  matrix.drawPixel(5, 1, led_set);matrix.writeDisplay();
  break;
  case 'O':
   
  matrix.drawPixel(6, 1, led_set);matrix.writeDisplay();
  break;
  case 'P':
   
  matrix.drawPixel(7, 1, led_set);matrix.writeDisplay();
  break;
  case 'Q':
   
  matrix.drawPixel(0, 2, led_set);matrix.writeDisplay();
  break;
  case 'R':
   
  matrix.drawPixel(1, 2, led_set);matrix.writeDisplay();
  break;
  case 'S':
   
  matrix.drawPixel(2, 2, led_set);matrix.writeDisplay();
  break;
  case 'T':
   
  matrix.drawPixel(3, 2, led_set);matrix.writeDisplay();
  break;
  case 'U':
   
  matrix.drawPixel(4, 2, led_set);matrix.writeDisplay();
  break;
  case 'V':
   
  matrix.drawPixel(5, 2, led_set);matrix.writeDisplay();
  break;
  case 'W':
   
  matrix.drawPixel(6, 2, led_set);matrix.writeDisplay();
  break;
  case 'X':
   
  matrix.drawPixel(7, 2, led_set);matrix.writeDisplay();
  break;
  case 'Y':
   
  matrix.drawPixel(0, 3, led_set);matrix.writeDisplay();
  break;
  case 'Z':
   
  matrix.drawPixel(1, 3, led_set);matrix.writeDisplay();
  break;
  case 'a':
   
  matrix.drawPixel(2, 3, led_set);matrix.writeDisplay();
  break;
  case 'b':
   
  matrix.drawPixel(3, 3, led_set);matrix.writeDisplay();
  break;
  case 'c':
   
  matrix.drawPixel(4, 3, led_set);matrix.writeDisplay();
  break;
  case 'd':
   
  matrix.drawPixel(5, 3, led_set);matrix.writeDisplay();
  break;
  case 'e':
   
  matrix.drawPixel(6, 3, led_set);matrix.writeDisplay();
  break;
  case 'f':
   
  matrix.drawPixel(7, 3, led_set);matrix.writeDisplay();
  break;
  case 'g':
   
  matrix.drawPixel(0, 4, led_set);matrix.writeDisplay();
  break;
  case 'h':
   
  matrix.drawPixel(1, 4, led_set);matrix.writeDisplay();
  break;
  case 'i':
   
  matrix.drawPixel(2, 4, led_set);matrix.writeDisplay();
  break;
  case 'j':
   
  matrix.drawPixel(3, 4, led_set);matrix.writeDisplay();
  break;
  case 'k':
   
  matrix.drawPixel(4, 4, led_set);matrix.writeDisplay();
  break;
  case 'l':
   
  matrix.drawPixel(5, 4, led_set);matrix.writeDisplay();
  break;
  case 'm':
   
  matrix.drawPixel(6, 4, led_set);matrix.writeDisplay();
  break;
  case 'n':
   
  matrix.drawPixel(7, 4, led_set);matrix.writeDisplay();
  break;
  case 'o':
   
  matrix.drawPixel(0, 5, led_set);matrix.writeDisplay();
  break;
  case 'p':
   
  matrix.drawPixel(1, 5, led_set);matrix.writeDisplay();
  break;
  case 'q':
   
  matrix.drawPixel(2, 5, led_set);matrix.writeDisplay();
  break;
  case 'r':
   
  matrix.drawPixel(3, 5, led_set);matrix.writeDisplay();
  break;
  case 's':
   
  matrix.drawPixel(4, 5, led_set);matrix.writeDisplay();
  break;
  case 't':
   
  matrix.drawPixel(5, 5, led_set);matrix.writeDisplay();
  break;
  case 'u':
   
  matrix.drawPixel(6, 5, led_set);matrix.writeDisplay();
  break;
  case 'v':
   
  matrix.drawPixel(7, 5, led_set);matrix.writeDisplay();
  break;
  case 'w':
   
  matrix.drawPixel(0, 6, led_set);matrix.writeDisplay();
  break;
  case 'x':
   
  matrix.drawPixel(1, 6, led_set);matrix.writeDisplay();
  break;
  case 'y':
   
  matrix.drawPixel(2, 6, led_set);matrix.writeDisplay();
  break;
  case 'z':
   
  matrix.drawPixel(3, 6, led_set);matrix.writeDisplay();
  break;
  case '{':
   
  matrix.drawPixel(4, 6, led_set);matrix.writeDisplay();
  break;
  case '}':
   
  matrix.drawPixel(5, 6, led_set);matrix.writeDisplay();
  break;
  case ':':
   
  matrix.drawPixel(6, 6, led_set);matrix.writeDisplay();
  break;
  case '<':
   
  matrix.drawPixel(7, 6, led_set);matrix.writeDisplay();
  break;
  case '>': 
   
  matrix.drawPixel(0, 7, led_set);matrix.writeDisplay();
  break;
  case '?': 
   
  matrix.drawPixel(1, 7, led_set);matrix.writeDisplay();
  break;
  case '[': 
   
  matrix.drawPixel(2, 7, led_set);matrix.writeDisplay();
  break;
  case ']': 
   
  matrix.drawPixel(3, 7, led_set);matrix.writeDisplay();
  break;
  case ';':
   
  matrix.drawPixel(4, 7, led_set);matrix.writeDisplay();
  break;
  case ',':
   
  matrix.drawPixel(5, 7, led_set);matrix.writeDisplay();
  break;
  case '.':
   
  matrix.drawPixel(6, 7, led_set);matrix.writeDisplay();
  break;
  case '/':
   
  matrix.drawPixel(7, 7, led_set);matrix.writeDisplay();
  break;
  
  // 기본 led 모양
  case '%':
  matrix.clear();
  matrix.drawBitmap(0, 0, love_bmp, 8, 8, 1);matrix.writeDisplay();    
  break;
  case '^':
  matrix.clear();
  matrix.drawBitmap(0, 0, smile_bmp, 8, 8, 1);matrix.writeDisplay();
  break;
  case '&':
  matrix.clear();
  matrix.drawBitmap(0, 0, neutral_bmp, 8, 8, 1);matrix.writeDisplay();
  break;
  case '*':
  matrix.clear();
  matrix.drawBitmap(0, 0, frown_bmp, 8, 8, 1);matrix.writeDisplay();
  break;
  case '(':
  matrix.clear();
  matrix.drawBitmap(0, 0, crossBig_bmp, 8, 8, 1);matrix.writeDisplay();
  break;
  
  case ')':
  matrix.clear();
  matrix.drawBitmap(0, 0, reset_bmp, 8, 8, 0);matrix.writeDisplay();
  break;  

  case '-':
  matrix.clear();
  break;

  case '=':   // led 제어 종료 
  cnt--;
  break;

  case'~':
  matrix.clear();
  matrix.blinkRate(1);
  matrix.drawRect(0,0, 8,8, 1);
  matrix.drawRect(1,1, 6,6, 2);
  matrix.fillRect(2,2, 4,4, 3);
  matrix.writeDisplay();
  break;
  
    }
  }
  cnt++;
  break;
  }
}
      if (measurement>10000){
        BTSerial.write(measurement);
        Serial.println(measurement);
      }

}

long TP_init(){

  long measurement=pulseIn (vibr_Pin, HIGH);  //wait for the pin to get HIGH and returns measurement
  return measurement;
}