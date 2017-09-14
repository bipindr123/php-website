import pandas as pd
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
from fbprophet import Prophet
import xlrd

# wb = xlrd.open_workbook('myfile.xlsx')
# sh = wb.sheet_by_index(0)

dates = [2014,2015,2016,2017,2018]
prices = [31, 35, 27, 20, 40]

# for rownum in range(0, sh.nrows):
#     row = sh.row_values(rownum)
#     for i, x in enumerate(row):
#         try:
#             row[i] = int(x)
#         except ValueError:
#             pass

#     print(row)

# dates = np.array(dates).reshape((len(dates), 1))

# print(dates)

# svr_len = SVR(kernel='rbf',C=1e3)

# svr_len.fit(dates, prices)

# plt.scatter(dates,prices,color='black',label='DATA')
# plt.plot(dates, svr_len.predict(dates), color ='red', label = 'RBF model')
# plt.xlabel('DATE')
# plt.ylabel('VALE')
# plt.title('HELLO ALL')
# plt.legend()
# plt.show()

def holt_alg(h, y_last, y_pred, T_pred, alpha, beta):
    pred_y_new = alpha * y_last + (1-alpha) * (y_pred + T_pred * h)
    pred_T_new = beta * (pred_y_new - y_pred)/h + (1-beta)*T_pred
    return (pred_y_new, pred_T_new)

def smoothing(t, y, alpha, beta):
    # initialization using the first two observations
    pred_y = y[1]
    pred_T = (y[1] - y[0])/(t[1]-t[0])
    y_hat = [y[0], y[1]]
    # next unit time point
    t.append(t[-1]+1)
    for i in range(2, len(t)):
        h = t[i] - t[i-1]
        pred_y, pred_T = holt_alg(h, y[i-1], pred_y, pred_T, alpha, beta)
        y_hat.append(pred_y)
    return y_hat

plt.plot(dates,prices, 'x-')
plt.hold(True)

pred_y = smoothing(dates, prices, alpha=.8, beta=.5)
plt.plot(dates[:10], pred_y, 'rx-')
plt.show()
