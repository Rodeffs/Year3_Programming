// C++ code
//
int buttonState = 0;

int lastButtonState = 0;

int toggle = 0;

void setup()
{
  pinMode(2, INPUT);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
}

void loop()
{
  buttonState = digitalRead(2);
  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      if (toggle == 0) {
        toggle = 1;
      } else {
        toggle = 0;
      }
    }
    delay(5); // Wait for 5 millisecond(s)
  }
  lastButtonState = buttonState;
  if (toggle == 1) {
    delay(250); // Wait for 250 millisecond(s)
    digitalWrite(13, HIGH);
    digitalWrite(12, LOW);
    delay(250); // Wait for 250 millisecond(s)
    digitalWrite(13, LOW);
    digitalWrite(12, HIGH);
  } else {
    digitalWrite(13, LOW);
    digitalWrite(12, LOW);
  }
}
