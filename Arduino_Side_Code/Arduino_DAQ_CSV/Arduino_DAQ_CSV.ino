// Arduino side code for data acquisition
// Assume Arduino connected to 4 Sensors ,On receiving appropriate characters,Arduino sends back Sensor values

// @ -> will trigger TransmitHumidityValue();       -> will send back humidity value
// # -> will trigger TransmitSoilMoistureValue();   -> will send back Soil-Moisture value
// $ -> will trigger Transmit_Temperature_Value();  -> will send back Temperature Value
// & -> will trigger TransmitLightIntensityValue(); -> will send back Light Sensor Value

// Functions are standin and user is supposed to implement them according to their needs 
// For Demo, the functions send a random number.


void setup() 
{
    Serial.begin(9600); //Data will be send to PC @9600bps
}

void loop() 
{
  char ReceivedByte; //
   
   if (Serial.available() > 0) //Wait for data reception
   {
     ReceivedByte = Serial.read();//Read data from Arduino Serial UART buffer
     
     switch(ReceivedByte)
     {
      case '@': //Serial.print('@');
                //Serial.print("HumidityValue ->");
                TransmitHumidityValue();
                break;
      case '$': //Serial.print('$');
                //Serial.print("4TemperatureValues ->");
                Transmit_Temperature_Value();
                break;
      case '#': //Serial.print('#');
                //Serial.print("SoilMoistureValue ->");
                TransmitSoilMoistureValue();
                break;
      case '&': //Serial.print('&');
                //Serial.print("LightIntensityValue -> ");
                TransmitLightIntensityValue();
                break;
      default:  Serial.println("Default Value");
     }//end of switch()
   }//end of if 
}//end of loop()



void TransmitHumidityValue(void)
{
  //Send Dummy Values using Random number generator for now 
  //Implement the code for talking with sensor here 
  
  long RandomNumber ;
  RandomNumber = random(40,90); //Generate Random number between 40 and 90
  Serial.println(RandomNumber); //Send Number followed by \n so python readline will exit on PC side 

}

void TransmitSoilMoistureValue(void)
{
  // Send Dummy Values using Random number generator for now 
  // Implement the code for talking with sensor here 
  long RandomNumber ;
  RandomNumber = random(30,50);// Generate Random number between 30 and 50
  Serial.println(RandomNumber);// Send Number followed by \n so python readline will exit on PC side 
}

void TransmitLightIntensityValue(void)
{
   // Send Dummy Values using Random number generator for now 
  // Implement the code for talking with sensor here 

  long RandomNumber ;
  RandomNumber = random(0,1024);// Generate Random number between 0 and 1024
  Serial.println(RandomNumber); // Send Number followed by \n so python readline will exit on PC side 
}


void Transmit_Temperature_Value(void)
{
  // Send Dummy Values using Random number generator for now 
  // Implement the code for talking with sensor here 

  long RandomNumber ;
  RandomNumber = random(20,90);// Generate Random number between 20 and 90
  Serial.println(RandomNumber);// Send Number followed by \n so python readline will exit on PC side 

}
