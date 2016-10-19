from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Dense, Flatten, Activation, Dropout, MaxPooling1D
from keras.optimizers import Adam, SGD
from keras.regularizers import l2
import h5py


def custom_keras_model(num_classes, weights_path=None, w_regularizer=None, b_regularizer=None, include_top = False):
    num_filters = 8
    num_pooling = 2
    num_filters_2 = 8
    filter_length = 3
    color_type = 3

    image_width, image_height = 224, 224 # For state farm images

    # Create callback for history report
    from keras.callbacks import Callback
    class LossHistory(Callback):
        def on_train_begin(self, logs={}):
            self.losses = []

        def on_batch_end(self, batch, logs={}):
            self.losses.append(logs.get('loss'))

    # from keras.utils.dot_utils import Grapher

    model = Sequential()
    # grapher = Grapher()

    # Now create the NN architecture (version 1)
    # Going with colour for now!!
    model.add(Convolution2D(num_filters, filter_length, filter_length, border_mode="valid",
                            activation="relu", name='conv1',
                            W_regularizer=w_regularizer, b_regularizer=b_regularizer,
                            input_shape=(color_type, image_width, image_height)))

    # Added
    model.add(MaxPooling2D(pool_size=(num_pooling, num_pooling)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(num_filters_2, filter_length, filter_length,
                            activation="relu", name='conv2',
                            W_regularizer=w_regularizer, b_regularizer=b_regularizer))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=(num_pooling, num_pooling)))
    model.add(Dropout(0.25))

    if include_top == True:
        model.add(Flatten())
        model.add(Dense(128,
                    W_regularizer=w_regularizer, b_regularizer=b_regularizer))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes,
                    W_regularizer=w_regularizer, b_regularizer=b_regularizer))
        model.add(Activation('softmax'))

    if weights_path:
        print "Loading weights from {}".format(weights_path)
        if include_top == True:
            model.load_weights(weights_path)
        # else:
        #     f = h5py.File(weights_path)
        #     layers = f.attrs['layer_names']
        #     nb_layers = len(layers)
        #     for k in range(0, nb_layers-1):     # for k in range(f.attrs['nb_layers']):
        #         if k >= len(model.layers):
        #             # we don't look at the last (fully-connected) layers in the savefile
        #             break
        #         layer_name = layers[k]
        #         g = f[layer_name]
        #         #g = f['layer_{}'.format(k)]
        #         weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
        #         model.layers[k].set_weights(weights)
        #     f.close()
        print('Model loaded.')

    # model.summary()
    # grapher.plot(model, 'nn_model.png')

    # TODO - Handle loading existing weights

    # if remove_top == True:
    #     print "Removing top fully connected layers"
    #     model.layers.pop()  # Remove top dense layer
    #     model.layers.pop()  # Remove the other dense layer

    return model, LossHistory

