import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

# Define paths
data_dir = './dataset'
categories = ['jute', 'maize', 'rice', 'sugarcane', 'wheat']  # Add your crop types

# Data loading and preprocessing
data = []
labels = []

for category in categories:
    path = os.path.join(data_dir, category)
    class_num = categories.index(category)
    for img_name in os.listdir(path):
        try:
            img_path = os.path.join(path, img_name)
            img_array = cv2.imread(img_path)
            img_array = cv2.resize(img_array, (224, 224))  # Resize images to 224x224 pixels
            data.append(img_array)
            labels.append(class_num)
        except Exception as e:
            print(f"Error loading image {img_name}: {e}")

# Convert to numpy arrays and normalize
data = np.array(data) / 255.0  # Normalize pixel values to [0, 1]
labels = np.array(labels)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)

# Save the preprocessed data
np.save('X_train.npy', X_train)
np.save('X_val.npy', X_val)
np.save('y_train.npy', y_train)
np.save('y_val.npy', y_val)