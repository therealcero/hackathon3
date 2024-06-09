import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Define categories
categories = ['jute', 'maize', 'rice', 'sugarcane', 'wheat']  # Replace with your actual crop types

# Load preprocessed data
X_train = np.load('X_train.npy')
X_val = np.load('X_val.npy')
y_train = np.load('y_train.npy')
y_val = np.load('y_val.npy')

# Build the Model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(len(categories), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the Model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the Model
epochs = 25
batch_size = 32
best_accuracy = 0.0  # Initialize best_accuracy

for epoch in range(epochs):
    print(f"Epoch {epoch + 1}/{epochs}")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=1,  # Train for 1 epoch at a time
        batch_size=batch_size,
        verbose=1
    )

    # Evaluate the Model
    loss, accuracy = model.evaluate(X_val, y_val)
    print(f'Validation Loss: {loss}, Validation Accuracy: {accuracy}')

    # Save the model if it's the best one so far
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        model.save('best_model.keras')
