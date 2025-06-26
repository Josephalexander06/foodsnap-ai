
# import numpy as np
# import tensorflow as tf
# import os, json, itertools
# import matplotlib.pyplot as plt
# from sklearn.metrics import classification_report, confusion_matrix
# import seaborn as sns


# MODEL_PATH ='foosnap_ai.h5'

# # Step 1: Load or train model
# if os.path.exists(MODEL_PATH):
#     print("✅ Model already exists. Loading saved model...")
#     model = tf.keras.models.load_model(MODEL_PATH)
# else:
#     print("🚀 Model not found. Training from scratch...")

#     training_folder = os.path.join('train_validation/train')
#     validation_folder = os.path.join('train_validation/validation')

#     training_set= tf.keras.utils.image_dataset_from_directory(
#         training_folder,
#         label_mode= 'categorical',
#         color_mode='rgb',
#         batch_size=16,
#         image_size=(224,224),
#         shuffle= True,
#     )

#     validation_set= tf.keras.utils.image_dataset_from_directory(
#         validation_folder,
#         label_mode= 'categorical',
#         color_mode='rgb',
#         batch_size=16,
#         image_size=(224,224),
#         shuffle= True,
#     )

#     cnn = tf.keras.models.Sequential()
#     cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[224,224,3]))
#     cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
#     cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
#     cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu'))
#     cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu'))
#     cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
#     cnn.add(tf.keras.layers.Flatten())
#     cnn.add(tf.keras.layers.Dense(units=512, activation='relu'))
#     cnn.add(tf.keras.layers.Dense(units=512, activation='relu'))
#     cnn.add(tf.keras.layers.Dropout(0.5))
#     cnn.add(tf.keras.layers.Dense(units=36, activation='softmax'))


#     cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
#     cnn.summary()

#     training_history = cnn.fit(x=training_set, validation_data = validation_set,epochs=36)

#     cnn.save('foosnap_ai.h5')
#     training_history.history

#     training_set.class_names

#     with open('training_history.json','w') as f:
#         json.dump(training_history.history,f)

#     print(training_history.history.keys())

#     print("Validation Set Accuracy: {}%" .format(training_history.history['val_accuracy'][-1]*100))
#     print("Training set Accuracy: {}" .format(training_history.history['accuracy'][-1]*100))

#     def get_true_labels_and_predictions(model,dataset):
#         true_labels = []
#         predicted_labels = []
#         for images, labels in dataset:
#             true_labels.extend(np.argmax(labels.np(),axis=1))
#             predicted_labels.extend(np.argmax(model.prediction(images),axis=1))
#         return true_labels, predicted_labels

#     train_true_labels,train_pred_labels = get_true_labels_and_predictions(cnn,training_set)
#     train_cm = confusion_matrix(train_true_labels,train_pred_labels)
#     train_report = classification_report(train_true_labels,train_pred_labels)


#     val_true_labels,val_pred_labels = get_true_labels_and_predictions(cnn,validation_set)
#     val_cm = confusion_matrix(val_true_labels,val_pred_labels)
#     val_report = classification_report(val_true_labels,val_pred_labels)

#     print("Train Confusion Matrix:")
#     print(train_cm)
#     print("Train Classification Report:")
#     print(train_report)

#     print("\nValidation Confusion Matrix:")
#     print(val_cm)
#     print("Validation Classification Report:")
#     print(val_report)


#     def normalize_confusion_matrix(cm):
#         rows_sum =cm.sum(axis = 1)
#         normalize_cm = cm / rows_sum[:,np.newaxis]
#         return normalize_cm

#     loaded_model =tf.keras.models.load_model('foosnap_ai.h5')



#     true_labels = []
#     predicted_labels = []

#     for images,labels in validation_set:
#         true_labels.extend(np.argmax(labels,axis=1))
#         prediction = loaded_model.predict(images)
#         predicted_labels.extend(np.argmax(prediction,axis=1))

#     class_names = validation_set.class_names
#     report = classification_report(true_labels,predicted_labels,target_names = class_names)

#     print('classification report:\n',report)

#     confusion = confusion_matrix(true_labels,predicted_labels)

#     def plot_confusion_matrix(cm,class_names):
#         plt.figure(figSize=(16,12))
#         plt.imshow(cm,interpolation = 'nearset',cmap = plt.cm.Blues)
#         plt.title('Confusion Matrix')
#         plt.colorbar()
#         tick_marks = np.arrage(len(class_names))
#         plt.xticks(tick_marks,class_names,rotation = 45)
#         plt.yticks(tick_marks,class_names)

#         fmt = 'd'
#         thresh = cm.max() / 2
#         for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#             plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

#         plt.ylabel('True label')
#         plt.xlabel('Predicted label')
#         plt.tight_layout()

#     plot_confusion_matrix(confusion, class_names)
#     plt.show()

#     train_cm_normalized = normalize_confusion_matrix(train_cm)
#     val_cm_normalized = normalize_confusion_matrix(val_cm)

#     def plot_normalized_confusion_matrix(cm,class_name):
#         plt.figure(figSize=(10,8))
#         sns.heatmap(cm,annot=True,xticklabels=class_names,yticklabels=class_names,cmap = 'Blues')
#         plt.title('Normalized Confusion Matrix')
#         plt.xlabel('Predicted Labels')
#         plt.ylabel('True Lables')
#         plt.show()

#     class_names = sorted(set(train_true_labels,val_true_labels))

#     plot_normalized_confusion_matrix(train_cm_normalized,class_names)
#     plot_normalized_confusion_matrix(val_cm_normalized,class_names)


#     num_samples_to_display = 9
#     sample_images, sample_labels = next(iter(validation_set.take(num_samples_to_display)))

#     # Get the corresponding class names from the test_set
#     class_names = validation_set.class_names

#     # Make predictions on the sampled images
#     sample_predictions = cnn.predict(sample_images)
#     sample_predictions = np.argmax(sample_predictions, axis=1)

#     # Display the images with their true and predicted labels
#     fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 10),
#                             subplot_kw={'xticks': [], 'yticks': []})

#     for i, ax in enumerate(axes.flat):
#         ax.imshow(sample_images[i].numpy().astype(np.uint8))
#         true_label = class_names[np.argmax(sample_labels[i])]
#         predicted_label = class_names[sample_predictions[i]]
#         print(predicted_label)
#         ax.set_title(f"True: {true_label}\nPredicted: {predicted_label}")

#     plt.tight_layout()
#     plt.show()

# # Expose these for import
# __all__ = ['cnn', 'validation_set']



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
model.summary()

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


