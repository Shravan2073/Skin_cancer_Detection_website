import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.utils import img_to_array
from PIL import Image
import numpy as np
import os

num_classes = 9
img_height = 180
img_width = 180

# Model definition
model = Sequential([
    layers.Input(shape=(img_height, img_width, 3)),
    layers.Rescaling(1.0/255)
])
model.add(Conv2D(32, 3, padding="same", activation='relu'))
model.add(MaxPool2D())

model.add(Conv2D(64, 3, padding="same", activation='relu'))
model.add(MaxPool2D())

model.add(Conv2D(128, 3, padding="same", activation='relu'))
model.add(MaxPool2D())
model.add(Dropout(0.15))

model.add(Conv2D(256, 3, padding="same", activation='relu'))
model.add(MaxPool2D())
model.add(Dropout(0.20))

model.add(Conv2D(512, 3, padding="same", activation='relu'))
model.add(MaxPool2D())
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation="relu"))
model.add(Dense(units=num_classes, activation='softmax'))

# Load the model weights
MODEL_PATH = "cnn_fc_model.weights.h5"
try:
    model.load_weights(MODEL_PATH)
except Exception as e:
    print(f"Error loading model weights: {e}")
    print(f"Attempted to load from path: {MODEL_PATH}")
    raise

# Define cancer types
cancer_types = [
    "Actinic Keratosis",
    "Basal Cell Carcinoma",
    "Dermatofibroma",
    "Melanoma",
    "Nevus",
    "Pigmented Benign Keratosis",
    "Seborrheic Keratosis",
    "Squamous Cell Carcinoma",
    "Vascular Lesion"
]

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert("RGB")  # Ensure it's RGB
    image = image.resize((img_height, img_width))
    arr = img_to_array(image)
    arr = arr[None, :, :, :]  # Add batch dimension
    return arr

def predict_cancer_type(image_path):
    # Preprocess the image and predict
    image_array = preprocess_image(image_path)
    prediction = model(image_array)

    # Convert prediction to a more readable format
    prediction = prediction.numpy().flatten()  # Flatten to 1D array

    # Find the index of the highest probability
    max_index = np.argmax(prediction)
    max_prob = prediction[max_index]

    return f"{cancer_types[max_index]} confidence {float(max_prob)}"
