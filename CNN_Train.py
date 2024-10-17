import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import os

def count_files_in_subdirectories(root_dir="TrainingSet"):
    sum_files = 0
    # Get the list of the all files in the folders
    subdirs = [d for d in os.listdir(root_dir) \
               if os.path.isdir(os.path.join(root_dir, d))]
    
    # Itterate in each of the folder
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        files_count = len([f for f in os.listdir(subdir_path) \
                           if os.path.isfile(os.path.join(subdir_path, f))])
        sum_files += files_count
    return sum_files

# Train a new CNN using information from TrainingSet directory
# Then return trained CNN
# TRAIN THE CNN    
def CNN_Train(train_dir):    
    # load the training image dataset into an ImageDatasGenerator
    # train_path contains the path to the dataset
    train_datagen = \
        tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(28, 28),
        # get the number of unique training labels in the training data
        batch_size=count_files_in_subdirectories(),
        class_mode='categorical',
        color_mode='grayscale'
    )
    
    # Define the CNN structure
    model = models.Sequential([
        # set the size of the input image as 28x28 pixels with 1 color 
        # channel (grayscale)
        layers.InputLayer(input_shape=(28, 28, 1)),
        # create the first convolution layer, it has 8 convolutional
        # filters, each with a height and width of 3 and input is 0 padded.
        # the input is padded with the appropriate number of zeros so that
        # the size of the output is the same size as the input.
        layers.Conv2D(8, (3, 3),    padding='same'),
        # normalize the output of the convolution between the range -1 
        # and 1. this prevents the updated weights from increasing 
        # explosively during training.
        layers.BatchNormalization(),
        # apply rectilinear unit activation function that sets all negative
        # values to zero
        layers.Activation('relu'),
        # apply max pooling using a pooling size of (2x2), and using a 
        # stride of 2
        layers.MaxPooling2D((2, 2), strides=2),
       
        # create a second convolution layer, it has 16 convolutional
        # filters, each filter has a height and width of 3 and the input is
        # zero padded.
        layers.Conv2D(16, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        # apply max pooling using a pooling size of (2x2), and using a 
        # stride of 2
        layers.MaxPooling2D((2, 2), strides=2),
        
        # create a third convolution layer, it has 32 convolutional
        # filters, each filter has a height and width of 3 and the input is
        # zero padded.
        layers.Conv2D(32, (3, 3), padding='same'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        
        layers.Flatten(),

        layers.Dense(train_generator.num_classes, 
                     # use a softmax layer to convert the outputs to a set of 
                     # probalities where each output represents the 
                     # probability that the image is a corresponding label.
                     activation='softmax')
    ])
    # END OF layers
    
    # optimizer to be used during training. In this case, 
    # the Adam optimizer is used. The optimizer is responsible for updating 
    # the model's weights during training based on the computed gradients. 
    # Adam is a popular optimization algorithm that adapts the learning 
    # rate during training.
    model.compile(optimizer=optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    # specify CNN training options
    model.fit(train_generator, epochs=700)
    
    return model


