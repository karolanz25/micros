from flask import Flask, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Convertir bytes recibidos a una imagen que OpenCV o tu modelo entiendan
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # AQUÍ LLAMAS A TU MODELO:
    # resultado = mi_modelo.predict(img)
    # Por ahora simulamos una respuesta:
    resultado = "plastico" 
    
    print(f"Residuo detectado: {resultado}")
    return resultado # Esto vuelve a la ESP32

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # El 0.0.0.0 es para que sea visible en la red local
