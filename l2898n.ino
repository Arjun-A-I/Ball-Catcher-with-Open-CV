#include<Stepper.h>
const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution,8,9,10,11);


void rotate(int num)
{
  num = 40-num;
  if(num>40)
  {
    myStepper.step(-400);
    delay(2000);
    myStepper.step(400);
  return;}
  int steps = num*10;
  myStepper.step(-steps);
  delay(2000);
  myStepper.step(steps);

}

void setup() {
    // Declare pins as Outputs
  Serial.begin(9600);
  Serial.setTimeout(10);
  myStepper.setSpeed(200);
  

}

void loop() {

    int a;
    while(Serial.available()){
      String data = Serial.readString();
      a = data.toInt();
//      Serial.println(a);

    rotate(a);
    }

}
