import cv2
import numpy as np
import matplotlib.pyplot as plot
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()
    print('number of folders = ', len(os.listdir(data_dir)))
    print()
    for folder in os.listdir(data_dir):
        print('number of images = ', len(os.listdir(os.path.join(data_dir,folder))))
        path = os.path.join(data_dir,folder)
        for imageName in os.listdir(path):
            images.append(
                cv2.resize( 
                    cv2.imread( os.path.join(path,imageName) ),
                   (IMG_WIDTH,IMG_HEIGHT) 
                )
            )
            labels.append( int(folder) )  # No tengo claro qué tipo debería tener para que lo entienda model.fit
    return (images,labels)
    # raise NotImplementedError


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.Sequential( name = "my model")

    model.add(tf.keras.Input(shape = (30,30,3) ) )     # 30x30 RGB images

    # model.add(tf.keras.layers.Flatten(input_shape = (30,30,3)))
    model.add(tf.keras.layers.Conv2D(3, 3, activation = "relu"))
    # model.add(tf.keras.layers.Conv2D(3, 3, activation = "relu"))
    model.add(tf.keras.layers.MaxPooling2D(3))
    model.add(tf.keras.layers.Conv2D(3, 3, activation = "relu"))
    # model.add(tf.keras.layers.Conv2D(3, 3, activation = "relu"))
    model.add(tf.keras.layers.MaxPooling2D( 2))

    # Classification layer
    model.add(tf.keras.layers.Dense(3)) # Para el dataset de pruebas
    # model.add(tf.keras.layers.Dense(42))

    print(model.summary())


    model.compile(
        optimizer = tf.keras.optimizers.RMSprop(),
        loss = tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics = [tf.keras.metrics.SparseCategoricalAccuracy()]
    )

    return model
    # raise NotImplementedError


# if __name__ == "__main__":
    # main()


############################## Testing ###############################


path = '.\\gtsrbSmall'
# path = '.\\gtsrb'
images,labels = load_data( path )

X_train, X_test, y_train, y_test = train_test_split(
    images, labels, test_size = 0.99
)

model   =   get_model()
# del(model)
# x0      =   tf.ones((30,30))
# print(model(x0))
# x       =   tf.ones((30,30,3))
# x = X_train[0]
# print(model(x))



# tf.keras.utils.plot_model(model,"model.png")

# model.fit(
#     X_train,
#     np.array(y_train),
# )

# To do -> convertir labels a np.array de floats
# To do -> revisar las dimensiones para el fit
# To do -> Debuggear fit para ver cómo funciona internamente
