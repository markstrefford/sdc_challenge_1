from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from keras import optimizers
import random
import sys
import numpy
import nnmodel

# The model from ai-tor
def create_model(optimizer='Adam' , init='normal', lr=0.01, loss="mse"):
    model = nnmodel.getNNModel()
    # other parameters can be set by adding more if statements if needed
    if optimizer == 'SGD':
        optimizers.optimizer(lr=lr,nesterov=True)
    else:
        optimizers.optimizer(lr=lr)
    model.compile(optimizer=optimizer, init=init)
    #model.compile()

# Randomn search could also be implemented but let's test this first
def grid_search(x,y, validation_split=0.4):
    seed = random.randint(0, sys.maxint)
    numpy.random.seed(seed)
    # create model
    model = KerasRegressor(build_fn=create_model, verbose=0)
    # grid search epochs, batch size and optimizer
    # feel free to adjust this stuffs to test more than I have here
    optimizers = ['SGD','RMSprop', 'Adam']
    init = ['glorot_uniform', 'normal', 'uniform', 'lecun_uniform', 'zero']
    lr = numpy.array([0.01,0.05,0.1])
    epochs = numpy.array([10, 100, 150, 200, 250])
    batches = numpy.array([5, 10, 20, 50, 100, 150, 200])

    param_grid = dict(lr=lr, optimizer=optimizers, nb_epoch=epochs, batch_size=batches, init=init)
    grid = GridSearchCV(estimator=model, param_grid=param_grid)
    grid_result = grid.fit(x, y)
    # summarize results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    # feel free to uncomment if you can afford to print all the results on your screen. Warning! It's gonna be pretty long
    #for params, mean_score, scores in grid_result.grid_scores_:
    #    print("%f (%f) with: %r" % (scores.mean(), scores.std(), params))
