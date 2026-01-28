import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# --- Configuración de parámetros ---
DATASET_PATH = 'dataset'  # Tu carpeta con las 6 subcarpetas
IMG_SIZE = (240, 240)
BATCH_SIZE = 32
EPOCHS = 10

# --- 1. Preprocesamiento y Aumento de Datos ---
# Usamos validación del 20% y aplicamos rotaciones para que el modelo sea más robusto
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.15,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# --- 2. Definición de la Arquitectura ---
# Cargamos MobileNetV2 pre-entrenado sin la capa superior (cabezal)
base_model = MobileNetV2(input_shape=(240, 240, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # No entrenamos las capas base para ir más rápido

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2), # Evita el sobreajuste
    layers.Dense(128, activation='relu'),
    layers.Dense(6, activation='softmax') # 6 clases: cardboard, glass, metal, paper, plastic, trash
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- 3. Entrenamiento ---
print("Iniciando entrenamiento...")
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# --- 4. Guardar el modelo y etiquetas ---
model.save('modelo_residuos_s3.h5')
print("¡Modelo guardado exitosamente como 'modelo_residuos_s3.h5'!")

# --- 5. Visualizar resultados ---
plt.plot(history.history['accuracy'], label='Precisión Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Precisión Validación')
plt.legend()
plt.show()
