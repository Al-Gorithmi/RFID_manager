#include <MFRC522.h>
#include <Servo.h>
#include <SPI.h>

Servo myServo;

const int pinSDA = 10;
const int pinRST = 9;

MFRC522 mfrc522(pinSDA,pinRST); 

String insertedTag ;

void setup() {
pinMode(3, OUTPUT);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
myServo.attach(6);
SPI.begin(); //Open SPI connection
mfrc522.PCD_Init(); // initializing proximity coupiling device
Serial.begin(9600);
myServo.write(0);
digitalWrite(3,LOW);
digitalWrite(5,LOW);
}

void loop() {
  digitalWrite(4,HIGH);
  if (mfrc522.PICC_IsNewCardPresent()) // true if RFID tag (PICC) is present PICC = proximity integrated circuit card
   {
    if (mfrc522.PICC_ReadCardSerial())//if card is read
    {
      //Serial.print("RFID tag :");
      for(byte i = 0; i<mfrc522.uid.size; i++)//read id
      {
        insertedTag.concat(String(mfrc522.uid.uidByte[i], HEX));                                   
      
        //Serial.println(mfrc522.uid.uidByte[i], HEX); //print id as hex values
        // Serial.print(" ");
      }
       Serial.println(insertedTag);
       delay(1050); 
      byte SerialData = Serial.read();
      if(SerialData == '1')
        {
         myServo.write(90);
         digitalWrite(5,HIGH);
         digitalWrite(4,LOW);
         delay(1000);
         }
                             
      else if (SerialData == '0')
         {
         myServo.write(0);
         digitalWrite(3,HIGH);
         digitalWrite(4,LOW);
         delay(1000);
          }
      }                             
      else 
        {
        Serial.println("ERROR");
        }              

  }
  insertedTag = "";
  digitalWrite(5,LOW);
  digitalWrite(3,LOW);
  
}
