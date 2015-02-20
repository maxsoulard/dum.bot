// Programme slave i2c commande servomotors pour AdafruitTrinket

#include <Wire.h>

void setup()
{
  Wire.begin(4);                // Joindre le Bus I2C avec adresse #4
  Wire.onReceive(receiveEvent); // enregistrer l'événement (lorsqu'une demande arrive)
}

void loop()
{
  delay(100);
}

void receiveEvent(int howMany)
{
  while(1 < Wire.available()) // Lire tous les octets sauf le dernier
  {
    char c = Wire.read();     // lecture de l'octet/byte comme caractère
	// Data : [U, D, R, L]. Si R ou L -> commande servo01. Sinon si U ou D -> commande servo02
	// TODO commande servo moteur + ou - 45°
  }
  int x = Wire.read();        // lecture de l'octet/byte ignoré comme un entier
}