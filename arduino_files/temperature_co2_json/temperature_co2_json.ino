/***************************************************************************
  This is a library for the CCS811 air

  This sketch reads the sensor

  Designed specifically to work with the Adafruit CCS811 breakout
  ----> http://www.adafruit.com/products/3566

  These sensors use I2C to communicate. The device's I2C address is 0x5A

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Dean Miller for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/
// worked well so far. send data as json 

#include "Adafruit_CCS811.h"
#include <math.h>
int a;
float temperature;
int B=3975;                  //B value of the thermistor
float resistance;
 
Adafruit_CCS811 ccs;

void setup() {
  Serial.begin(9600);

//  Serial.println("CCS811 test");

  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }

  // Wait for the sensor to be ready
  while(!ccs.available());
}

void loop() {
  if(ccs.available()){
    if(!ccs.readData()){
          a=analogRead(0);
    resistance=(float)(1023-a)*10000/a; //get the resistance of the sensor;
    temperature=1/(log(resistance/10000)/B+1/298.15)-273.15;//convert to temperature via datasheet&nbsp;;


    //  Serial.print("CO2: ");
     // Serial.print(ccs.geteCO2());
    //  Serial.print("ppm, TVOC: ");
    //  Serial.println(ccs.getTVOC());

   String data = "{\"CO2\": " + String(ccs.geteCO2()) +  "," + "\"Temperature\": " + String(temperature) + "," +  "\"TVOC\": " + String(ccs.getTVOC()) +"}";
      Serial.println(data);

    }
    else{
      Serial.println("ERROR!");
      while(1);
    }
  }
  delay(1000);
}
