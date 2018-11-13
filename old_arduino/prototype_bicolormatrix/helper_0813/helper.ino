#include <gfxfont.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SPITFT.h>
#include <Adafruit_SPITFT_Macros.h>

#include <Adafruit_LEDBackpack.h>
#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2,3); // SoftwareSerial(TX, RX)
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

/*
 * PORT CONNECTION
 * 
 * A4 - Bicolormatrix SDA
 * A5 - Bicolormatrix SCL
 * 2 - Bluetooth TX
 * 3 - Bluetooth RX
 * 
 */


///////////// DEFINE LED MATRIX START /////////////
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

///////////// DEFINE LED MATRIX END /////////////

void setup() {
  BTSerial.begin(9600);
  Serial.begin(9600);
  matrix.begin(0x70);

  matrix.clear();

  // BLINK LED
  matrix.drawRect(0,0, 8,8, 1);
  matrix.drawRect(1,1, 6,6, 2);
  matrix.fillRect(2,2, 4,4, 3);
  matrix.writeDisplay();matrix.clear();
  matrix.drawRect(0,0, 8,8, 1);
  matrix.drawRect(1,1, 6,6, 2);
  matrix.fillRect(2,2, 4,4, 3);
  matrix.writeDisplay();
}

void loop() {
  int signal = BTSerial.read();

  switch(signal) {
    case '%': // LED -> LOVE
      matrix.clear();
      matrix.drawBitmap(0, 0, love_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case '^': // LED -> SMILE
      matrix.clear();
      matrix.drawBitmap(0, 0, smile_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case '&': // LED -> NEUTRAL
      matrix.clear();
      matrix.drawBitmap(0, 0, neutral_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case '*': // LED -> FROWN
      matrix.clear();
      matrix.drawBitmap(0, 0, frown_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case '(': // LED -> CROSSBIG
      matrix.clear();
      matrix.drawBitmap(0, 0, crossBig_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case ')': // LED -> RESET
      matrix.clear();
      matrix.drawBitmap(0, 0, reset_bmp, 8, 8, 1);matrix.writeDisplay();
      break;

    case 'b': // LED -> BLINK STOP
      matrix.blinkRate(0);
      break;

    case 'B': // LED -> BLINK START
      matrix.blinkRate(1);
      break;

    case'~': // LED -> RECT BLINK
      matrix.clear();
      matrix.blinkRate(1);
      matrix.drawRect(0,0, 8,8, 1);
      matrix.drawRect(1,1, 6,6, 2);
      matrix.fillRect(2,2, 4,4, 3);
      matrix.writeDisplay();
      break;
  }
}
