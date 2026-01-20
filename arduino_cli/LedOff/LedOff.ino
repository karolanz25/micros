
// Definición de estados según la arquitectura
#if defined(ESP8266)
  // El ESP8266 (NodeMCU) tiene lógica invertida
  #define LED_ON  LOW
  #define LED_OFF HIGH
#else
  // Arduino Uno, ESP32 y la mayoría de placas usan lógica directa
  #define LED_ON  HIGH
  #define LED_OFF LOW
#endif

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, LED_OFF); // Siempre apagará
}
