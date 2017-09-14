import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

dates = [[1, 17], [2, 17], [3, 17]]
dates2 = [[4, 17], [5, 17]]
prices = [55, 44, 23]


def predict_price(dates, prices, dates2):
    dates = np.reshape(dates, (len(dates), 2))  # converting to matrix of n X 1
    dates2 = np.reshape(dates2, (len(dates2), 2))  # converting to matrix of n X 1

    # defining the support vector regression models
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(dates, prices)  # fitting the data points in the models

    # plotting the initial datapoints
    #plt.scatter(dates, prices, color='black', label='Data')
    # plotting the line made by the RBF kernel
    plt.plot(dates2,svr_rbf.predict(dates2), color='red', label='RBF model')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()

    return svr_rbf.predict(x)[0]


# get_data('goog.csv') # calling get_data method by passing the csv file to it
print("Dates- ", dates)
print("Prices- ", prices)

predicted_price = predict_price(dates, prices, dates2)
print("\nThe stock open price for 29th Feb is:")
print("RBF kernel: $", str(predicted_price[0]))
