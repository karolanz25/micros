# --- Variables configurables ---
SKETCH ?= LedOff
PORT ?= /dev/ttyACM0
# Valores comunes: arduino:avr:uno, esp8266:esp8266:nodemcuv2, esp32:esp32:esp32s3
BOARD ?= arduino:avr:uno

# --- Colores ---
YELLOW = \033[0;33m
RESET  = \033[0m
# --- Comandos ---
.PHONY: all compile upload list

# 1. Listar placas conectadas
list:
	@echo "Buscando placas conectadas..."
	arduino-cli board list

# 2. Crear un nuevo sketch (Uso: make new SKETCH=nombre_nuevo)
new:
	@arduino-cli sketch new $(SKETCH)
	@echo "Sketch '$(SKETCH)' creado con éxito."

# 3. Compilar
compile:
	@echo "$(YELLOW)Compilando $(SKETCH) para $(BOARD)...$(RESET)"
	arduino-cli compile --fqbn $(BOARD) $(SKETCH)

# 4. Subir
upload:
	@echo "$(YELLOW)Subiendo a $(BOARD) en el puerto $(PORT)...$(RESET)"
	arduino-cli upload -p $(PORT) --fqbn $(BOARD) $(SKETCH)

# 5. Todo en uno: Compilar y Subir
all: compile upload

# 6. Ayuda rápida
help:
	@echo "Uso del Makefile:"
	@echo "  make list                  - Listar placas detectadas"
	@echo "  make new SKETCH=nombre     - Crear un sketch nuevo"
	@echo "  make compile SKETCH=nom BOARD=fqbn - Solo compilar"
	@echo "  make upload SKETCH=nom PORT=/dev/ttyX BOARD=fqbn - Solo subir"
	@echo "  make all SKETCH=nom PORT=/dev/ttyX BOARD=fqbn - Compilar y subir"
