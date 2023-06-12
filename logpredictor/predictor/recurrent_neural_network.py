import os

import numpy as np
import pandas as pd
from keras.layers import Dense, LSTM
from keras.models import Sequential

from datasets.log_dataset import LogDataset


class RecurrentNeuralNetwork:
    def __init__(self, dataset: LogDataset, n_features: int, n_steps: int, n_width: int):
        self.dataset = dataset
        self.n_features = n_features
        self.n_steps = n_steps
        self.n_width = n_width
        self.model = None
        self.x = None
        self.X = None

    def __prepare_data(self):
        self.x = self.dataset.inputs
        self.path = os.path.abspath('').replace('\\', '/').replace('recurrent_neural_network', 'tmp')
        data = pd.read_csv(self.path + '/tmp/report_parser_out.csv')
        X = []
        for i in range(len(data) - self.n_steps):
            seq_x = self.x[1:1 + self.n_steps]
            X.append(seq_x)
        self.X = np.array(X)

    def __build_model(self):
        self.model = Sequential()
        self.model.add(LSTM(64, activation='tanh', input_shape=(self.n_steps, self.n_features)))
        self.model.add(Dense(self.n_features))
        self.model.compile(optimizer='adam', loss='mae')
        self.model.fit(self.X[:], self.x[self.n_steps:], epochs=20, verbose=1)

    def __write_csv(self, forecast: np.ndarray):
        timestamp = self.dataset.last_timestamp
        first_column = np.zeros(self.n_width)
        for i in range(self.n_width):
            timestamp += 300000
            first_column[i] = timestamp
        forecast = np.c_[first_column, forecast]
        np.savetxt(self.path + '/tmp/rnn_out.csv', forecast, delimiter=',', fmt='%1.3f')

    def get_predictions(self):
        self.__prepare_data()
        self.__build_model()
        x_input = self.x[-self.n_steps:]
        forecast = np.zeros((self.n_width, self.n_features))
        for i in range(self.n_width):
            x_input_reshaped = x_input.reshape((1, self.n_steps, self.n_features))
            yhat = self.model.predict(x_input_reshaped, verbose=0)
            for j in range(self.n_features):
                yhat[0, j] = max(yhat[0, j], 0)
            forecast[i] = yhat
            x_input = np.vstack([np.delete(x_input, 0, axis=0), yhat])
        forecast = (forecast.T * self.dataset.std + self.dataset.mean).T
        for i in range(self.n_features):
            if i not in [9, 10, 11, 14]:
                forecast[:, i] = np.int32(forecast[:, i])
        self.__write_csv(forecast)
