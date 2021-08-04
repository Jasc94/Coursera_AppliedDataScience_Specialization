import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import colors
from matplotlib import cm       # feature pairplot (scatter matrix)
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D         # 3D plots

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


############################# Module 1 #############################
#### Decision boundaries
def plot_fruit_knn(X, y, n_neighbors, h = .05):
    # Create color maps
    cmap_light = colors.ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF','#AFAFAF'])
    cmap_bold  = colors.ListedColormap(['#FF0000', '#00FF00', '#0000FF','#AFAFAF'])

    # Model selection and training
    model = KNeighborsClassifier(n_neighbors = n_neighbors, weights = "uniform", n_jobs = -1)
    model.fit(X, y)
    print("Step 1: Model training - Finished")

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max] -> plot axes (not features)
    x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:, 0].max() + 1
    y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:, 1].max() + 1

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))


    # Predict all the points (that will be later plotted as areas)
    prediction = model.predict(np.c_[xx.ravel(), yy.ravel()])
    print("Step 2: Model prediction - Finished")
    # Reshape so that it can be plotted
    prediction = prediction.reshape(xx.shape)
    print("Step 3: Prediction reshape - Finished")

    # Put the result into a color plot
    plt.figure()
    # To plot the colored areas
    plt.pcolormesh(xx, yy, prediction, cmap = cmap_light)

    # To plot the actual training points
    plt.scatter(X.iloc[:, 0], X.iloc[:, 1], s = 50, c = y, cmap = cmap_bold, edgecolor = "black")

    # Axes limits
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    patch0 = mpatches.Patch(color='#FF0000', label='apple')
    patch1 = mpatches.Patch(color='#00FF00', label='mandarin')
    patch2 = mpatches.Patch(color='#0000FF', label='orange')
    patch3 = mpatches.Patch(color='#AFAFAF', label='lemon')
    plt.legend(handles=[patch0, patch1, patch2, patch3])

    plt.xlabel(X.iloc[:, 0].name)
    plt.ylabel(X.iloc[:, 1].name)
    
    plt.show()