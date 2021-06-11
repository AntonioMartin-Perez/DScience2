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
                ) / 255.0               # Pixel value rescaling from 0-255 to 0-1
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
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu',input_shape = (IMG_HEIGHT,IMG_WIDTH,3)),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        # tf.keras.layers.Flatten( input_shape = (30,30,3) ), # Asume que la primera dimensión es la remesa (batch) y no la toca
        tf.keras.layers.Dense(128, activation = 'relu'),
        tf.keras.layers.Dense(NUM_CATEGORIES)   # NUM_CATEGORIES = 43
    ])

    model.compile( optimizer = 'adam',
                    loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True),   # Inicialmente usaba SparseCategoricalCrossentropy pero no funciona si he metido los labels en forma de matriz (después de aplicarle un to_categorical_)
                    metrics = ['accuracy'])

    # model.summary()
    return model
    # raise NotImplementedError


if __name__ == "__main__":
    main()


# ############################## Testing ###############################


# # path = '.\\gtsrbSmall'
# path = '.\\gtsrb'
# images,labels = load_data( path )

# X_train, X_test, y_train, y_test = train_test_split(
    # np.array(images), np.array(labels), test_size = TEST_SIZE
# )

# # Como el enunciado pedía listas, los datos salen en listas de arrays y tengo que convertirlos para hacer fit

# model   =   get_model()

# model.fit(X_train,y_train, epochs = 10)

# "Test accuracy"
# test_loss, test_acc = model.evaluate( X_test, y_test, verbose = 2)
# print('\nTest accuracy:', test_acc)

# "Adding a softmax layer we can convert logits to probabilities"
# probability_model = tf.keras.Sequential([model,tf.keras.layers.Softmax()])  
# predictions = probability_model.predict(X_test[0:10])
# predictions[0]                                          # Probabilidades de que sea de cada tipo
# np.max(predictions[0]),np.argmax(predictions[0])        # (probabilidad máxima, categoría)
# y_test[0]


# """
# ############################### Appendix ##############################
# "https://www.tensorflow.org/tutorials/keras/classification#build_the_model"

# "Mostrar una imagen"
# plot.figure()
# plot.imshow(X_train[1])
# plot.colorbar()
# plot.grid(False)
# plot.show()

# "Mostrar varias imágenes"
# plot.figure(figsize=(10,10))
# for i in range(25):
#     plot.subplot(5,5,i+1)
#     plot.xticks([])
#     plot.yticks([])
#     plot.grid(False)
#     plot.imshow(X_train[i], cmap=plot.cm.binary)
#     plot.xlabel(y_train[i])
# plot.show()


# "Gráficas"
# def plot_image(i, predictions_array, true_label, img):
#   true_label, img = true_label[i], img[i]
#   plot.grid(False)
#   plot.xticks([])
#   plot.yticks([])

#   plot.imshow(img, cmap=plot.cm.binary)

#   predicted_label = np.argmax(predictions_array)
#   if predicted_label == true_label:
#     color = 'blue'
#   else:
#     color = 'red'

#   plot.xlabel("{} {:2.0f}% ({})".format(predicted_label,
#                                 100*np.max(predictions_array),
#                                 true_label),
#                                 color=color)

# def plot_value_array(i, predictions_array, true_label):
#   true_label = true_label[i]
#   plot.grid(False)
#   plot.xticks(range(43))
#   plot.yticks([])
#   thisplot = plot.bar(range(43), predictions_array, color="#777777")
#   plot.ylim([0, 1])
#   predicted_label = np.argmax(predictions_array)

#   thisplot[predicted_label].set_color('red')
#   thisplot[true_label].set_color('blue')


# i = 7
# plot.figure(figsize=(20,3))
# plot.subplot(1,2,1)
# plot_image(i, predictions[i], y_test, X_test)
# plot.subplot(1,2,2)
# plot_value_array(i, predictions[i],  y_test)
# plot.show()


# """