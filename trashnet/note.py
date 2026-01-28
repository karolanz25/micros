import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices("GPU")

if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✓ Enabled memory growth for {len(gpus)} GPU(s)")
    except RuntimeError as e:
        print("⚠️ Memory growth must be set before TensorFlow initializes GPUs")
        print(e)
else:
    print("⚠️ No GPU found, running on CPU")


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from tensorflow import keras
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.applications import (
    EfficientNetB3, EfficientNetB4, ResNet50V2, 
    DenseNet121, InceptionV3, MobileNetV2
)
from tensorflow.keras.layers import (
    Dense, Dropout, GlobalAveragePooling2D, BatchNormalization,
    Conv2D, MaxPooling2D, Flatten, Activation
)

# Sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_recall_fscore_support
)
from sklearn.utils import class_weight

# Visualization
import cv2
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Config:
    """Centralized configuration for the entire pipeline"""
    
    # Paths
    DATA_PATH = './dataset'
    OUTPUT_PATH = './working'
    
    # Image Parameters
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    IMG_CHANNELS = 3
    IMG_SIZE = (IMG_HEIGHT, IMG_WIDTH)
    
    # Training Parameters
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 1e-4
    
    # Data Split
    VALIDATION_SPLIT = 0.15
    TEST_SPLIT = 0.15
    
    # Model Parameters
    DROPOUT_RATE = 0.5
    L2_REG = 1e-4
    
    # Callbacks
    EARLY_STOPPING_PATIENCE = 10
    REDUCE_LR_PATIENCE = 5
    REDUCE_LR_FACTOR = 0.5
    
config = Config()

print("\n" + "=" * 80)
print("PROJECT CONFIGURATION")
print("=" * 80)
for attr in dir(config):
    if not attr.startswith('_'):
        print(f"{attr:30s}: {getattr(config, attr)}")
print("=" * 80)

from pathlib import Path
import pandas as pd

# Dataset root (Kaggle path)
DATASET_ROOT = "/home/karo/Documents/Github/micros/trashnet/dataset"

IMG_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def load_split_dataframe(root_dir, split):
    """
    Load images and labels from a dataset split into a DataFrame.

    Returns a DataFrame with:
        - filepath: full image path
        - label: class name (folder name)
    """
    split_dir = Path(root_dir) / split
    data = []

    for img_path in split_dir.rglob("*"):
        if img_path.suffix.lower() in IMG_EXTENSIONS:
            data.append({
                "filepath": str(img_path),
                "label": img_path.parent.name
            })

    return pd.DataFrame(data)


# Load datasets
train_df = load_split_dataframe(DATASET_ROOT, "train")
val_df   = load_split_dataframe(DATASET_ROOT, "val")
test_df  = load_split_dataframe(DATASET_ROOT, "test")




print("Train samples:", len(train_df))
print("Validation samples:", len(val_df))
print("Test samples:", len(test_df))

print("\nTrain class distribution:")
print(train_df["label"].value_counts())



class_names = sorted(train_df["label"].unique())
label_to_id = {name: idx for idx, name in enumerate(class_names)}

train_df["label_id"] = train_df["label"].map(label_to_id)
val_df["label_id"]   = val_df["label"].map(label_to_id)
test_df["label_id"]  = test_df["label"].map(label_to_id)
