#include <TinyWireS.h>
#include <Adafruit_SoftServo.h>  // SoftwareServo (works on non PWM pins)

#define I2C_SLAVE_ADDRESS 0x04
#define PIN_TRIG 3
#define PIN_ECHO 4
#define SERVO1PIN 1

//Adafruit_SoftServo myServo1;
//int16_t  servo1Position;

byte reg[] = {0x00, 0x00};
byte reg_idx = 0;

long lecture_echo;
long cm;

void onRequest()
{
  TinyWireS.send(reg[reg_idx]);
  reg_idx = (reg_idx == 1) ? 0 : 1; 
}

void setup()
{
    // Servomotor setup
    /*OCR0A = 0xAF;            // any number is OK
    TIMSK |= _BV(OCIE0A);    // Turn on the compare interrupt (below!)
    myServo1.attach(SERVO1PIN);   // Attach the servo to pin 1 on Trinket
    servo1Position = 20;
    myServo1.write(servo1Position);
    tws_delay(200);
    servo1Position = 120;
    myServo1.write(servo1Position);
    tws_delay(200);*/
    
    // I2C setup
    TinyWireS.begin(I2C_SLAVE_ADDRESS);
    TinyWireS.onRequest(onRequest);
    
    // HC-SR04 setup
    pinMode(PIN_TRIG, OUTPUT);
    digitalWrite(PIN_TRIG, LOW);
    pinMode(PIN_ECHO, INPUT);
}

void loop()
{
    digitalWrite(PIN_TRIG, HIGH);
    delayMicroseconds(100);
    digitalWrite(PIN_TRIG, LOW);
    lecture_echo = pulseIn(PIN_ECHO, HIGH);
    cm = lecture_echo / 58;
    
    reg[0] = lowByte(cm);
    reg[1] = highByte(cm);

    TinyWireS_stop_check();
    //myServo1.write(servo1Position+40);
    //tws_delay(15);
}

// Adafruit :
// We'll take advantage of the built in millis() timer that goes off
// to keep track of time, and refresh the servo every 20 milliseconds
// The SIGNAL(TIMER0_COMPA_vect) function is the interrupt that will be
// Called by the microcontroller every 2 milliseconds
/*volatile uint8_t counter = 0;
SIGNAL(TIMER0_COMPA_vect) {
    // this gets called every 2 milliseconds
    counter += 2;
    // every 20 milliseconds, refresh the servos!
    if (counter >= 20) {
      counter = 0;
      myServo1.refresh();
    }
}*/
