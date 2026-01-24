from camera import Camera, GrabMode, PixelFormat, FrameSize, GainCeiling
# Para cámara asíncrona
#from acamera import Camera, GrabMode, PixelFormat, FrameSize, GainCeiling

cam = Camera(data_pins=[11, 9, 8, 10, 12, 18, 17, 16],pclk_pin=13,vsync_pin=6,href_pin=7,xclk_pin=15,sda_pin=4,scl_pin=5,pixel_format=PixelFormat.JPEG,frame_size=FrameSize.QVGA,jpeg_quality=90,fb_count=2,grab_mode=GrabMode.LATEST)

cam.init()

import socket
import network
import time

# Configuración WiFi
SSID = 'Claro_0699E3'
PASSWORD = 'T4R9W8X2J9F8'
PC_IP = '192.168.20.42'  # <--- PON AQUÍ LA IP DE TU PC
PORT = 5005

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(1)

print("Conectado. Enviando a:", PC_IP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

take_photo = True
while take_photo:
    buf = cam.capture()
    if buf:
        # Enviamos el memoryview directamente
        # Nota: Si la imagen es muy grande para UDP (>64KB),
        # considera usar TCP o bajar la resolución a QVGA.
        sock.sendto(buf, (PC_IP, PORT))

        # IMPORTANTE: Liberar el buffer según tu librería
        # cam.free_buffer()
        cam.free_buffer()
        take_photo = False
    time.sleep(0.1) # Ajusta para controlar los FPS
