import cv2
import socket
import numpy as np

UDP_IP = "0.0.0.0" # Escuchar en todas las interfaces
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Esperando streaming...")

while True:
    # Recibimos el paquete de datos
    data, addr = sock.recvfrom(65507) 
    
    # Convertimos los bytes a una matriz de imagen
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is not None:
        cv2.imshow('ESP32-S3 Stream', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
