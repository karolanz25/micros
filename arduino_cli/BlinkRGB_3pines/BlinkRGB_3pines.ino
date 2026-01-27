#define PIN_TAKE_PIC 47
#define PIN_R 38
#define PIN_G 39
#define PIN_B 40

void setup() {
  // put your setup code here, to run once:
  pinMode(PIN_TAKE_PIC, INPUT);
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  fijarColor(0,0,0);
}

// Función para mezclar (R, G, B de 0 a 255)
void fijarColor(int r, int g, int b) {
  analogWrite(PIN_R, r);
  analogWrite(PIN_G, g);
  analogWrite(PIN_B, b);
}
void loop() {
  //fijarColor(128, 200, 0); // Amarillo
  //fijarColor(0, 255, 255); // Cyan
  //fijarColor(128, 0, 255); // Morado
  //fijarColor(100, 110, 0); // Naranja
  //fijarColor(180, 255, 255); // Blanco
  if( digitalRead(PIN_TAKE_PIC) == HIGH ){
    fijarColor(0,255,0);  
  } else {
    fijarColor(128, 0, 255);
  }
  delay(10);
}
