import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('best_model.keras')

# Load the validation data
X_val = np.load('X_val.npy')
y_val = np.load('y_val.npy')

# Evaluate the model on the validation data
loss, accuracy = model.evaluate(X_val, y_val)

# Print the results
print(f'Validation Loss: {loss}')
print(f'Validation Accuracy: {accuracy}')
