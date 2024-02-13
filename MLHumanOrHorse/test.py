import os
# Remember to put the folders of images in the same foler as the code 
# Directory with our training horse pictures
train_horse_dir = 'horse-or-human/horses'
# Directory with our training human pictures
train_human_dir = 'horse-or-human/humans'
# Directory with our training horse pictures
validation_horse_dir = 'validation-horse-or-human/horses'
# Directory with our training human pictures
validation_human_dir = 'validation-horse-or-human/humans'
train_horse_names = os.listdir('horse-or-human/horses')
#print(train_horse_names[:10])
train_human_names = os.listdir('horse-or-human/humans')
#print(train_human_names[:10])
validation_horse_hames = os.listdir('validation-horse-or-human/horses')
#print(validation_horse_hames[:10])
validation_human_names = os.listdir('validation-horse-or-human/humans')
#print(validation_human_names[:10])
import tensorflow as tf
model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(100, 100, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fourth convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class
    # ('horses') and 1 for the other ('humans')
    tf.keras.layers.Dense(1, activation='sigmoid')
])
from  keras.optimizers import RMSprop  
optimizer = RMSprop(lr=0.0001)
model.compile(loss='binary_crossentropy',
              optimizer=optimizer,
              metrics=['acc'])

from keras.preprocessing.image import ImageDataGenerator

# All images will be augmented according to whichever lines are uncommented
# below. We can first try without any of the augmentation beyond the rescaling
train_datagen = ImageDataGenerator(
      rescale=1./255,
      #rotation_range=40,
      #width_shift_range=0.2,
      #height_shift_range=0.2,
      #shear_range=0.2,
      #zoom_range=0.2,
      #horizontal_flip=True,
      #fill_mode='nearest'
      )

# Flow training images in batches of 128 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        'horse-or-human/',  # This is the source directory for training images
        target_size=(100, 100),  # All images will be resized to 100x100
        batch_size=128,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

validation_datagen = ImageDataGenerator(rescale=1./255)

validation_generator = validation_datagen.flow_from_directory(
        'validation-horse-or-human',
        target_size=(100, 100),
        class_mode='binary')

history = model.fit(
      train_generator,
      steps_per_epoch=8,
      epochs=10,
      verbose=1,
      validation_data=validation_generator)

import numpy as np
from tensorflow.keras import utils
import cv2
import keyboard
import time
#------------------ predicting images---------------#
case=''#'capture' #<----------- select your use method ('capture'for screen capture, else for normal image recognition)
if(case=='capture'):
    #--------------------this is for a camera capture--------------#
    vid = cv2.VideoCapture(0) 
    
    while(True): 
        ret, frame = vid.read()  
        img = cv2.resize(frame, (100,100))
        x = utils.img_to_array(img)
        x = x / 255.0
        x = np.expand_dims(x, axis=0)

        image_tensor = np.vstack([x])
        classes = model.predict(image_tensor)
        print(classes[0])
        if classes[0]<0.5:
            print( " is a human")
        else:
            print( " is a horse")
        time.sleep(0.1)
        #!!!!!!!!---press 'esc' to exit the camera capture---!!!!!!!#
        if keyboard.is_pressed('esc'):
            break;
else:
    img = utils.load_img('hooman.jpeg', target_size=(100, 100))
    x = utils.img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)

    image_tensor = np.vstack([x])
    classes = model.predict(image_tensor)
    print(classes[0])
    if classes[0]>0.5:
        print(" is a Horse")
    else:
        print(" is a Human")

