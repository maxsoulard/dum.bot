/**
 * Example sketch for writing to and reading from a slave in transactional manner
 *
 * NOTE: You must not use delay() or I2C communications will fail, use tws_delay() instead (or preferably some smarter timing system)
 *
 * On write the first byte received is considered the register addres to modify/read
 * On each byte sent or read the register address is incremented (and it will loop back to 0)
 *
 * You can try this with the Arduino I2C REPL sketch at https://github.com/rambo/I2C/blob/master/examples/i2crepl/i2crepl.ino 
 * If you have bus-pirate remember that the older revisions do not like the slave streching the clock, this leads to all sorts of weird behaviour
 *
 * To read third value (register number 2 since counting starts at 0) send "[ 8 2 [ 9 r ]", value read should be 0xBE
 * If you then send "[ 9 r r r ]" you should get 0xEF 0xDE 0xAD as response (demonstrating the register counter looping back to zero)
 *
 * You need to have at least 8MHz clock on the ATTiny for this to work (and in fact I have so far tested it only on ATTiny85 @8MHz using internal oscillator)
 * Remember to "Burn bootloader" to make sure your chip is in correct mode 
 */


/**
 * Pin notes by Suovula, see also http://hlt.media.mit.edu/?p=1229
 *
 * DIP and SOIC have same pinout, however the SOIC chips are much cheaper, especially if you buy more than 5 at a time
 * For nice breakout boards see https://github.com/rambo/attiny_boards
 *
 * Basically the arduino pin numbers map directly to the PORTB bit numbers.
 *
// I2C
arduino pin 0 = not(OC1A) = PORTB <- _BV(0) = SOIC pin 5 (I2C SDA, PWM)
arduino pin 2 =           = PORTB <- _BV(2) = SOIC pin 7 (I2C SCL, Analog 1)
// Timer1 -> PWM
arduino pin 1 =     OC1A  = PORTB <- _BV(1) = SOIC pin 6 (PWM)
arduino pin 3 = not(OC1B) = PORTB <- _BV(3) = SOIC pin 2 (Analog 3)
arduino pin 4 =     OC1B  = PORTB <- _BV(4) = SOIC pin 3 (Analog 2)
 */
#define I2C_SLAVE_ADDRESS 0x4 // the 7-bit address (remember to change this when adapting this example)
// Get this from https://github.com/rambo/TinyWire
#include <TinyWireS.h>
#include <Adafruit_SoftServo.h>
// The default buffer size, Can't recall the scope of defines right now
#ifndef TWI_RX_BUFFER_SIZE
#define TWI_RX_BUFFER_SIZE ( 16 )
#define SERVO1PIN 4
#define SERVO2PIN 1
#endif

Adafruit_SoftServo myServo1, myServo2;
int16_t  servo1Position;
int16_t  servo2Position;
boolean servo1TurnLeft;
boolean servo1TurnRight;
boolean servo2TurnUp;
boolean servo2TurnDown;

volatile uint8_t i2c_regs[] =
{
    0xDE, 
    0xAD, 
    0xBE, 
    0xEF, 
};
// Tracks the current register pointer position
volatile byte reg_position;
const byte reg_size = sizeof(i2c_regs);

/**
 * This is called for each read request we receive, never put more than one byte of data (with TinyWireS.send) to the 
 * send-buffer when using this callback
 */
void requestEvent()
{  
    TinyWireS.send(i2c_regs[reg_position]);
    // Increment the reg position on each read, and loop back to zero
    reg_position++;
    if (reg_position >= reg_size)
    {
        reg_position = 0;
    }
}

/*Actions du servo moteur1*/
void turnRight() {
  int16_t servo1PositionTemp = servo1Position - 20;
  if (servo1PositionTemp > 180 || servo1PositionTemp < 0) {
      return;
  }
  else if (servo1PositionTemp >= 160){
     servo1PositionTemp += 20;
     servo1PositionTemp -= 5;
  }
  else if (servo1PositionTemp >= 175){
     servo1PositionTemp == 180;
  }
  myServo1.write(servo1PositionTemp);
  servo1Position = servo1PositionTemp;
}

void turnLeft() {
  int16_t servo1PositionTemp = servo1Position + 20;
  if (servo1PositionTemp > 180 || servo1PositionTemp < 0) {
      return;
  }
  else if (servo1PositionTemp >= 160){
     servo1PositionTemp -= 20;
     servo1PositionTemp += 5;
  }
  else if (servo1PositionTemp >= 175){
     servo1PositionTemp == 180;
  }
  myServo1.write(servo1PositionTemp);
  servo1Position = servo1PositionTemp;
}

void turnUp() {
}

void turnDown() { 
}

/*TODO : actions du servo moteur2*/

/**
 * The I2C data received -handler
 *
 * This needs to complete before the next incoming transaction (start, data, restart/stop) on the bus does
 * so be quick, set flags for long running tasks to be called from the mainloop instead of running them directly,
 */
void receiveEvent(uint8_t howMany)
{
    if (howMany < 1)
    {
        // Sanity-check
        return;
    }
    if (howMany > TWI_RX_BUFFER_SIZE)
    {
        // Also insane number
        return;
    }

    reg_position = TinyWireS.receive();
    howMany--;
    if (!howMany)
    {
        // This write was only to set the buffer for next read
        return;
    }
    boolean instructionServo = false;
    while(howMany--)
    {
        i2c_regs[reg_position] = TinyWireS.receive();
        
        if (reg_position == 2) {
            if (i2c_regs[reg_position] == 'l') {
              servo1TurnLeft = true;
            }
            else if (i2c_regs[reg_position] == 'r') {
              servo1TurnRight = true;
            }
            else if (i2c_regs[reg_position] == 'u') {
              servo2TurnUp = true;
            }
            else if (i2c_regs[reg_position] == 'd') {
              servo2TurnDown = true;
            }
        }
        
        reg_position++;
        if (reg_position >= reg_size)
        {
            reg_position = 0;
        }
    }
}


void setup()
{
    servo1TurnLeft = false;
    // TODO: Tri-state this and wait for input voltage to stabilize     
    //pinMode(SERVO1PIN, OUTPUT); // OC1A, also The only HW-PWM -pin supported by the tiny core analogWrite
    
    /**
     * Reminder: taking care of pull-ups is the masters job
     */

    TinyWireS.begin(I2C_SLAVE_ADDRESS);
    TinyWireS.onReceive(receiveEvent);
    
    OCR0A = 0xAF;            // any number is OK
    TIMSK |= _BV(OCIE0A);    // Turn on the compare interrupt (below!)
  
    servo1Position = 90;
    myServo1.attach(SERVO1PIN);
    myServo1.write(servo1Position);           // Tell servo to go to position per quirk
    delay(500);
    
    pinMode(3, OUTPUT); // OC1B-, Arduino pin 3, ADC
    digitalWrite(3, LOW);
}

void loop()
{
    if (servo1TurnLeft){
        turnLeft();
        servo1TurnLeft = false;
    }
    if (servo1TurnRight){
        turnRight();
        servo1TurnRight = false;
    }
    if (servo2TurnUp){
        turnUp();
        servo2TurnUp = false;
    }
    if (servo2TurnDown){
        turnDown();
        servo2TurnDown = false;
    }
    /**
     * This is the only way we can detect stop condition (http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&p=984716&sid=82e9dc7299a8243b86cf7969dd41b5b5#984716)
     * it needs to be called in a very tight loop in order not to miss any (REMINDER: Do *not* use delay() anywhere, use tws_delay() instead).
     * It will call the function registered via TinyWireS.onReceive(); if there is data in the buffer on stop.
     */
    TinyWireS_stop_check();
}

// We'll take advantage of the built in millis() timer that goes off
// to keep track of time, and refresh the servo every 20 milliseconds
// The SIGNAL(TIMER0_COMPA_vect) function is the interrupt that will be
// Called by the microcontroller every 2 milliseconds
volatile uint8_t counter = 0;
SIGNAL(TIMER0_COMPA_vect) {
  // this gets called every 2 milliseconds
  counter += 2;
  // every 20 milliseconds, refresh the servos!
  if (counter >= 20) {
    counter = 0;
    myServo1.refresh();
  }
}
