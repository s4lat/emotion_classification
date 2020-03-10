#include <TimerOne.h>

#define PULSE_PIN A0

int data0 = 0;
int data1 = 0;

int hits_counter = 0;

unsigned long t0 = 0;
unsigned long t1 = 0;
float pulse = 0.0;
int PULSE_STATE = 0;

void sendData() {
  if (PULSE_STATE == 0){
    t0 = millis();
    PULSE_STATE = 1;
  }
  
  data1 = data0;
  data0 = map(analogRead(PULSE_PIN), 0, 1023, 0, 2);

  if (data0 > data1 && data1 == 0){
    hits_counter += 1;
  }

  if (PULSE_STATE == 1 && (millis() - t0) / 1000.0 > 5.0){
    pulse = hits_counter * 12.0;
    PULSE_STATE = 0;
    hits_counter = 0;
  }

  Serial.print("P");
  Serial.print(pulse);
  Serial.print("p");

}

// функция setup вызывается однократно при запуске Arduino
void setup() {
  Serial.begin(115200);
  Timer1.initialize(3000);
  Timer1.attachInterrupt(sendData);
}

void loop() {
}
