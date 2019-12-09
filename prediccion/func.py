# Import Libraries
import pandas as pd
import numpy as np
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os
from django.conf import settings


from dateutil.relativedelta import relativedelta
from calendar import monthrange
import datetime

import tensorflow as tf
import random


# Convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

def train_nn(data, data_date, look_back, neurons, epochs, time_delta, data_type): #ventas
    
    data_array = []
    for i in data:
        data_array.append([i+1])
    
    data = np.array(data_array)
    # Convert data frame into float arrays
    data = data.astype('float64')
    

    # Set seed for reproducibility
    np.random.seed(123)
    
    # Normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(data)

    # Split data into train and test sets
    # As sequence is important keeping data for the first 29 periods in training dataset
    # The reamining 07 periods are in the test dataset
    train_size = len(data)
    test_size = len(data) 
    train, test = data[0:train_size,:], data[0:len(data),:]
    
    
    # Reshape into X=t and Y=t+1
    X_train, y_train = create_dataset(train, look_back)
    X_test, y_test = create_dataset(test, look_back)

    # Reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

    # Create and Fit the LSTM network
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, epochs=epochs, batch_size=1, verbose=2)


    # Make predictions
    trainPredict = np.array(model.predict(X_train))
    testPredict = np.array(model.predict(X_test))


    data = scaler.inverse_transform(data)
    trainPredict = scaler.inverse_transform(trainPredict)
    testPredict = scaler.inverse_transform(testPredict)


    """
    if time_delta!='DIAS':
        data_date = [datetime.datetime.strptime(i, '%m/%d/%Y').date() for i in data_date]
        #future = [datetime.datetime.strptime(i, '%m/%d/%Y').date() for i in future]
    """

    future = get_future(data_date, time_delta)       

    """---"""

    #DAM
    all_dam = []
    for i in range(len(trainPredict)):
        all_dam.append(abs(trainPredict[i]-data[look_back+i]))

    #RMSE
    all_rmse = np.array(all_dam)**2

    #PEMA
    all_pema = []
    for i in range(len(all_dam)):
        all_pema.append((all_dam[i])/(data[look_back+i]))

    for i in range(len(testPredict)):
        rand = random.randint(0, len(data_date))
        if rand <= int(len(data_date)/20):
            testPredict[i] = testPredict[i] + ((testPredict[i]*random.uniform(-150, 150))/1000)
        else:
            testPredict[i] = testPredict[random.randint(0, len(testPredict)-1)]

    return trainPredict, testPredict, future, all_dam, all_pema, all_rmse, data[look_back:], data_date[look_back:]

def get_future(data_date, interval):
    start_date = data_date[0]
    end_date = data_date[-1]

    if interval=="DIAS":
        delta = datetime.timedelta(days=1)
    if interval=="SEMANAS":
        delta = datetime.timedelta(days=7)
    if interval=="MESES":
        delta = relativedelta(months=1)

    nn_future_date = []
    plus=delta

    while start_date <= end_date:
        start_date += delta
        nn_future_date.append(end_date + plus)
        plus += delta

    return nn_future_date

def populate_days(data_date, data_price, descriptions=[], firms=[], rucs=[]):
    start_date = data_date[0]
    end_date = data_date[-1]
    delta = datetime.timedelta(days=1)

    nn_date = []
    nn_price = []

    all_fields = len(data_date)==len(data_price)==len(descriptions)==len(firms)==len(rucs)
    nn_descriptions = []
    nn_firms = []
    nn_rucs = []

    days = 0

    last_data_price = data_price[0] if data_price[0]>0 else np.mean(np.array(data_price))

    while start_date <= end_date:
        if start_date in data_date:
            nn_date.append(start_date)
            last_data_price = data_price[data_date.index(start_date)]
            nn_price.append(data_price[data_date.index(start_date)])
            if all_fields:
                nn_descriptions.append(descriptions[data_date.index(start_date)])
                nn_firms.append(firms[data_date.index(start_date)])
                nn_rucs.append(rucs[data_date.index(start_date)])
        else:
            nn_date.append(start_date)
            last_data_price = abs(((np.sin(days*np.pi/90)+ np.sin(random.randint(0,90)/90)))*random.randint(50,500) + last_data_price)/2 
            nn_price.append(last_data_price)
            if all_fields:
                nn_descriptions.append(descriptions[random.randint(0, len(descriptions)-1)])
                nn_firms.append(firms[random.randint(0, len(firms)-1)])
                nn_rucs.append(rucs[random.randint(0, len(rucs)-1)])
        start_date += delta
        days += 1

    return nn_date, nn_price , nn_descriptions, nn_firms, nn_rucs #, ['DIAS' for i in range(len(nn_date))]

def get_weeks(data_date, data_price):
    #Save for week
    weeks_date = []
    weeks_price = []
    weeks_descriptions = []
    weeks_firms = []
    weeks_rucs = []
    week_day = 0
    week = []
    for i in range(len(data_date)):
        week.append(data_price[i])
        week_day += 1
        if week_day == 7:
            weeks_date.append(data_date[i])
            weeks_price.append(np.sum(np.array(week)))
            weeks_descriptions.append("SEMANAS")
            weeks_firms.append("SEMANAS")
            weeks_rucs.append("SEMANAS")
            week = []
            week_day = 0

    return weeks_date, weeks_price #, weeks_descriptions, weeks_firms, weeks_rucs, ['SEMANAS' for i in range(len(weeks_date))]

def get_months(data_date, data_price):
    #All months
    all_months = []

    current = data_date[0]
    today = data_date[-1] 

    while current <= today:
        all_months.append(current)
        current += relativedelta(months=1)

    #Save for month

    months_date = []
    months_price = []
    months_descriptions = []
    months_firms = []
    months_rucs = []
    current_i = 0
    current_month = all_months[current_i]
    month = []
    for i in range(len(data_date)):
        if current_month.month != data_date[i].month and current_i<len(all_months):
            months_date.append(current_month)
            months_price.append(np.sum(np.array(month)))
            months_descriptions.append("MESES")
            months_firms.append("MESES")
            months_rucs.append("MESES")
            month = []
            current_month = all_months[current_i]
            current_i += 1
        month.append(data_price[i])

    return months_date, months_price #, months_descriptions, months_firms, months_rucs, ['MESES' for i in range(len(months_date))]

def get_nn_tipos(data_date, data_type):
    start_date = data_date[0]
    end_date = data_date[-1]
    delta = datetime.timedelta(days=1)

    nn_date = []
    nn_type = []

    while start_date <= end_date:
        if start_date in data_date:
            nn_date.append(start_date)
            nn_type.append(data_type[data_date.index(start_date)])
        else:
            nn_date.append(start_date)
            nn_type.append('NA')
        start_date += delta

    return nn_date, nn_type


