class Config:
    """Centralized configuration for the entire pipeline"""
    
    # Paths
    DATA_PATH = '/kaggle/input/garbage-classification'
    OUTPUT_PATH = '/kaggle/working'
    
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


