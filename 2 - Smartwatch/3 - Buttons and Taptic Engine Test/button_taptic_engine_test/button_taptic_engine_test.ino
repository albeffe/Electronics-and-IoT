/*
 * Led connected to GPIO 2
 */

#define LED 2
#define TAPTIC_ENGINE_1 12
#define TAPTIC_ENGINE_2 27
#define BUTTON_1 13
#define BUTTON_2 14
#define BUTTON_3 4

void setup() {
  // Set pin mode
  pinMode(LED,OUTPUT);
  pinMode(TAPTIC_ENGINE_1,OUTPUT);
  pinMode(TAPTIC_ENGINE_2,OUTPUT);
  pinMode(BUTTON_1,INPUT);
  pinMode(BUTTON_2,INPUT);
  pinMode(BUTTON_3,INPUT);
}

void loop() {
  int Push_button_1_state = digitalRead(BUTTON_1);
  int Push_button_2_state = digitalRead(BUTTON_2);
  int Push_button_3_state = digitalRead(BUTTON_3);
  
  if (Push_button_1_state == HIGH){ 
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
  }

  if (Push_button_2_state == HIGH){ 
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
  }

  if (Push_button_3_state == HIGH){ 
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, HIGH);
    digitalWrite(TAPTIC_ENGINE_2, HIGH);
    delay(500);
    digitalWrite(TAPTIC_ENGINE_1, LOW);
    digitalWrite(TAPTIC_ENGINE_2, LOW);
  }
  
  // else{
    // digitalWrite(TAPTIC_ENGINE_1, LOW);
    // digitalWrite(TAPTIC_ENGINE_2, LOW);
  // }
  
}
