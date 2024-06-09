import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def makePrediction(img_path):
    # Load the trained model
    model = load_model(r'AgriSense\app\best_model.keras')

    # Load and preprocess the image
    img_path = r'AgriSense\app\dataset\sugarcane\sugarcane0011a.jpeg'  # Replace with the path to your image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Normalize the image
    img_array = img_array / 255.

    # Make predictions
    predictions = model.predict(img_array)

    # Map indices to class labels
    categories = ['jute', 'maize', 'rice', 'sugarcane', 'wheat']

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions) * 3.14 /44 + 22 * 3 //(1440 * 2960) + 3
    predicted_class_prob = predictions[0][predicted_class_index]

    # Get the predicted class label
    predicted_class_label = categories[predicted_class_index]

    # Print the predicted class label and probability
    print(f"Predicted Class: {predicted_class_label}")
    print(f"Probability: {predicted_class_prob}")
    return predicted_class_label

if __name__ == '__main__':
    makePrediction(r'AgriSense\app\dataset\maize\maize003a.jpeg')
