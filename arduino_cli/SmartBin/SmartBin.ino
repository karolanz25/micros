/**
  digitalWrite(RGB_BUILTIN, HIGH);  // Turn the RGB LED white
  delay(1000);
  digitalWrite(RGB_BUILTIN, LOW);  // Turn the RGB LED off
  delay(1000);

  rgbLedWrite(RGB_BUILTIN, RGB_BRIGHTNESS, 0, 0);  // Red
  delay(1000);
**/
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// --- Configuración de Pines y Objetos ---
#define PIN_TAKE_PIC 47
#define PIN_R 38
#define PIN_G 39
#define PIN_B 40

// ===========================
// Select camera model in board_config.h
// ===========================
#include "board_config.h"

// ===========================
// Enter your WiFi credentials
// ===========================
const char *ssid = "Claro_0699E3";
const char *password = "T4R9W8X2J9F8";
const char *serverName = "http://192.168.20.42:5000/predict"; // IP de tu PC

bool ultimoEstado = LOW;

// Semáforo para avisar a la tarea que tome la foto
SemaphoreHandle_t xSemaforoFoto;

//void startCameraServer();
//void setupLedFlash();

void setup() {
  pinMode(PIN_TAKE_PIC, INPUT_PULLDOWN);
  pinMode(PIN_R, OUTPUT);
  pinMode(PIN_G, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  fijarColor(128, 200, 0); // Amarillo
  //fijarColor(0, 0, 0); // Off
  //fijarColor(128, 200, 0); // Amarillo
  //fijarColor(0, 255, 255); // Cyan
  //fijarColor(128, 0, 255); // Morado
  //fijarColor(100, 110, 0); // Naranja
  //fijarColor(180, 255, 255); // Blanco


  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();
  
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  //config.frame_size = FRAMESIZE_UXGA;
  config.frame_size = FRAMESIZE_QVGA; // 320x240: Ideal para IA
  config.pixel_format = PIXFORMAT_JPEG;  // for streaming
  //config.pixel_format = PIXFORMAT_RGB565; // for face detection/recognition
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if (config.pixel_format == PIXFORMAT_JPEG) {
    if (psramFound()) {
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }

#if defined(CAMERA_MODEL_ESP_EYE)
  pinMode(13, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
#endif
  
  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) { 
    Serial.printf("Camera init failed with error 0x%x", err);
    return; 
  }

  sensor_t *s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);        // flip it back
    s->set_brightness(s, 1);   // up the brightness just a bit
    s->set_saturation(s, -2);  // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if (config.pixel_format == PIXFORMAT_JPEG) {
    s->set_framesize(s, FRAMESIZE_QVGA);
  }

#if defined(CAMERA_MODEL_M5STACK_WIDE) || defined(CAMERA_MODEL_M5STACK_ESP32CAM)
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);
#endif

#if defined(CAMERA_MODEL_ESP32S3_EYE)
  s->set_vflip(s, 1);
#endif

// Setup LED FLash if LED pin is defined in camera_pins.h
#if defined(LED_GPIO_NUM)
  setupLedFlash();
#endif

  WiFi.begin(ssid, password);
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  Serial.print("WiFi connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  fijarColor(128, 0, 255); // Morado
}

// Función para mezclar (R, G, B de 0 a 255)
void fijarColor(int r, int g, int b) {
  analogWrite(PIN_R, r);
  analogWrite(PIN_G, g);
  analogWrite(PIN_B, b);
}

void clasificarResiduo() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) return;

  HTTPClient http;
  http.begin(serverName);
  http.addHeader("Content-Type", "image/jpeg");

  // Enviamos los bytes de la imagen directamente
  int httpResponseCode = http.POST(fb->buf, fb->len);

  if (httpResponseCode > 0) {
    String payload = http.getString(); // Aquí recibes "plastico", "metal", etc.
    Serial.println("Resultado: " + payload);
    //moverServo(payload); // Tu función para mover los motores
  }
  
  http.end();
  esp_camera_fb_return(fb); // ¡Importante para no agotar la RAM!
}

void loop() {
  bool estadoActual = digitalRead(PIN_TAKE_PIC);
  
  if (estadoActual == HIGH && ultimoEstado == LOW) {
    delay(50);
    fijarColor(0, 255, 255); // Cyan
    Serial.println("Botón presionado. Iniciando captura...");
    clasificarResiduo();
    fijarColor(128, 0, 255); // Morado
  } 
  ultimoEstado = estadoActual;
}
