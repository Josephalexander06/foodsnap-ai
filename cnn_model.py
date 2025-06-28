import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D, Input
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt


print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))


MODEL_PATH ='model_saved.h5'

training_folder = os.path.join('train_validation/train')
validation_folder = os.path.join('train_validation/validation')



# imageHeight = 224
# imageWidth = 224
# thickness = 3
# inputShape = (imageHeight,imageWidth,thickness)

imageDataGenerator = ImageDataGenerator(rescale = 1./255,
                                        featurewise_center=True,
                                        featurewise_std_normalization=True,
                                        horizontal_flip = True ,
                                        rotation_range = 15,
                                        width_shift_range = 0.2,
                                        height_shift_range = 0.2,
                                        zoom_range = 0.1
                                        )

testDataGenerator = ImageDataGenerator(rescale=1./255)

trainGenerator = imageDataGenerator.flow_from_directory(training_folder,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=True)

validGenerator = imageDataGenerator.flow_from_directory(validation_folder,
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    shuffle=False  
    )
# print(trainGenerator.class_indices)

fruitMap = dict([(v,k) for k, v in trainGenerator.class_indices.items()])
class_names_list = [fruitMap[i] for i in range(len(fruitMap))]
class_names_no = len(class_names_list)


model =Sequential()
model.add(Input(shape=(224, 224, 3))) 
model.add(Conv2D(64,(5,5), activation = 'relu', padding = 'Same'))
model.add(Conv2D(64,(5,5), activation = 'relu', padding = 'Same'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), activation='relu', padding='Same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='Same'))
model.add(MaxPooling2D((2, 2), strides=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(class_names_no, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(1e-3), metrics=['accuracy'])
# model.summary()

if os.path.exists(MODEL_PATH):
    print("✅ Model already exists. Loading saved model...")
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    print("🚀 Model not found. Training from scratch...")

    early = tf.keras.callbacks.EarlyStopping(monitor = 'vali_accuracy',patience = 3, mode = 'max',restore_best_weights=True)
    history = model.fit(trainGenerator, validation_data=validGenerator,
                        steps_per_epoch=trainGenerator.n//trainGenerator.batch_size,
                            validation_steps=validGenerator.n//validGenerator.batch_size,
                            callbacks=[early],
                        epochs=30)

    model.save('model_saved.h5')

model = load_model('model_saved.h5')


def predict_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0) 

    prediction = model.predict(image)

    # plt.title("Original Image")
    # plt.axis('off')  # Optional: hides the axes
    # plt.show()  
    predicted_index = np.argmax(prediction[0])
    confidence = prediction[0][predicted_index] * 100
    predicted_label = class_names_list[predicted_index]
 

    top_3_indices = prediction[0].argsort()[-3:][::-1]
    for i in top_3_indices:
        print(f"{class_names_list[i]}: {prediction[0][i]*100:.2f}%")

    print(f"This image is {predicted_label} with a {confidence:.2f}% confidence.")
 
    return predicted_label


