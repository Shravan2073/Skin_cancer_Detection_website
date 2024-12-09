from PIL import Image
import numpy as np

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess the image for model input.
    
    :param image_path: Path to the image file
    :param target_size: Tuple of (width, height) for resizing
    :return: Preprocessed image as a numpy array
    """
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def validate_image(image_path):
    """
    Validate if the file is a valid image.
    
    :param image_path: Path to the image file
    :return: Boolean indicating if the file is a valid image
    """
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except:
        return False

