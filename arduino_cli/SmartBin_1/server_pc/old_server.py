from flask import Flask, request
import cv2
import numpy as np
import tensorflow as tf
# from PIL import Image
import io
import time

app = Flask(__name__)

model = tf.keras.models.load_model('modelo_residuos_s3.h5')
labels = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Cargar los bytes
        nparr = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("Foto capturada")

        if img is None:
            print("Error: No se pudo decodificar la imagen")
            return "error_imagen", 400

        # 2. Preprocesamiento CRÍTICO para 240x240
        # Convertimos BGR (OpenCV) a RGB (TensorFlow)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Redimensionamos exactamente a lo que espera tu modelo reentrenado
        img_resizada = cv2.resize(img_rgb, (240, 240)) 

        # 3. Normalización y Ajuste de Dimensiones
        # El modelo espera (None, 240, 240, 3). El expand_dims añade el "1" inicial.
        img_final = img_resizada / 255.0
        img_final = np.expand_dims(img_final, axis=0)

        # 4. Inferencia
        pred = model.predict(img_final)
        indice = np.argmax(pred)
        clase_detectada = labels[indice]
        
        timestamp = int(time.time())
        nombre_archivo = f"capturas/{clase_detectada}_{timestamp}.jpg"

        cv2.imwrite(nombre_archivo, img)

        print(f"Predicción exitosa: {clase_detectada} con {np.max(pred)*100:.2f}% de certeza")
        
        return clase_detectada

    except Exception as e:
        # Esto te dirá exactamente qué falló en la consola de Linux
        print(f"Error interno en la predicción: {e}")
        return "error_servidor", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # El 0.0.0.0 es para que sea visible en la red local
