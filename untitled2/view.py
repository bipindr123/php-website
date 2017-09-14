from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from http.server import HTTPServer, SimpleHTTPRequestHandler, test as test_orig
import threading
import time
import sys
import os
import xlrd
import simplejson as json
import json
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from django.http import JsonResponse



# Create your views here.
from untitled2 import settings


# for using linear regression
def predict_price2(dates, prices, dates2):
    genius_regression_model = LinearRegression()
    genius_regression_model.fit(dates, prices)
    return genius_regression_model.predict(dates2)


# for using rbf regression
def predict_price(dates, prices, dates2):
    # defining the support vector regression models
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(dates, prices)  # fitting the data points in the models

    return svr_rbf.predict(dates2)


def con():
    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook('./myfile.xlsx')
    sh = wb.sheet_by_index(0)

    # List to hold dictionaries
    output = {}
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        row = sh.row_values(rownum)
        col = sh.row_values(0)
        for i, x in enumerate(row):
            try:
                row[i] = int(x)
            except ValueError:
                pass

        if (row[0] != ""):
            boss = row[0]
            output.update(
                {row[0]: {row[1]: dict(zip(col[2:], row[2:]))}})
        else:
            output[boss].update({row[1]: dict(zip(col[2:], row[2:]))})

    # Serialize the list of dicts to JSON
    j = json.dumps(output)

    # Write to file
    with open('data.json', 'w') as f:
        f.write(j)
    finalai()


class mythread2(threading.Thread):
    def run(self):
        con()
        print("file changer  is running")
        i = os.path.getmtime('./puthere/myfile.xlsx')
        while (True):
            if i != os.path.getmtime('./puthere/myfile.xlsx'):
                con()
                i = os.path.getmtime('./puthere/myfile.xlsx')
                print("the file has changed")
            time.sleep(1)


def finalai():
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11, "Dec": 12}
    monthAsString = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    output = {}
    with open('data.json') as data_file:
        data = json.load(data_file)

    flag = 0
    for i in data:
        flag = 0
        for j in data[i]:
            output2 = {}
            # print(j)
            dates = []
            values = []
            dates2 = []

            for k, v in data[i][j].items():
                x = ([months[k.split('-')[0]], int(k.split('-')[1])])
                dates.append(x)
                values.append(v)
            dates2.append([dates[-1][0], dates[-1][1]])
            dates2[0][0] = dates2[0][0] + 1
            dates2.append([dates2[0][0] + 1, dates2[0][1]])
            # print(dates2)
            # print(dates)
            # print(values)
            dates3 = []

            try:
                next_val = predict_price(dates, values, dates2)
            except:
                pass
            dates3 = []
            for e in range(0, len(dates2)):
                dates3.append(monthAsString[dates2[e][0]] + '-' + str(dates2[e][1]))
                output2.update({dates3[e]: next_val[e]})
            # print(output2)
            for l in dates3:
                flag2 = 0
                if flag == 0:
                    output.update({i: {j: output2}})
                else:
                    output[i].update({j: output2})
                flag = 1

    j = json.dumps(output)

    # Write to file
    with open('data2.json', 'w') as f:
        f.write(j)

def getsjason(request):
    backup_path = "/home/beagle/untitled2/data.json"
    return HttpResponse(open(backup_path, 'r'), content_type='application/json; charset=utf8').has_header('Access-Control-Allow-Origin', '*')

def getsjason2(request):
    backup_path = os.path.join(".", "data2.json")
    return HttpResponse(open(backup_path, 'r'), content_type='application/json; charset=utf8')

def index(request):
    runthis()
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request,'index.html')

def runthis():
    e = mythread2()
    e.start()
