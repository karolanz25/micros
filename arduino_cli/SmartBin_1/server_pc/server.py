from flask import Flask, request
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = Flask(__name__)

model = tf.keras.models.load_model('modelo_residuos_s3.h5')
labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

@app.route('/predict', methods=['POST'])
def predict():
    # Convertir bytes recibidos a una imagen que OpenCV o tu modelo entiendan
    nparr = np.frombuffer(request.data, np.uint8)
    #img = Image.open(nparr)
    #img = img.resize((224, 224))
    #img_array = np.array(img) / 255.0
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    clase_detectada = labels[np.argmax(pred)]
    print(clase_detectada)
    # Por ahora simulamos una respuesta:
    #resultado = "plastico"
    resultado = clase_detectada
    
    print(f"Residuo detectado: {resultado}")
    return resultado # Esto vuelve a la ESP32

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # El 0.0.0.0 es para que sea visible en la red local
