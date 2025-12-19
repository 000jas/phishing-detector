import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

def train_lstm(X, y):
    model = Sequential([
        Embedding(5000, 128),
        LSTM(128),
        Dense(1, activation="sigmoid")
    ])
    model.compile("adam", "binary_crossentropy", ["accuracy"])
    model.fit(X, y, epochs=3, batch_size=32)
    model.save("models/lstm_model.h5")

def train_cnn(X, y):
    model = Sequential([
        Embedding(8000, 128),
        Conv1D(128, 5, activation="relu"),
        GlobalMaxPooling1D(),
        Dense(1, activation="sigmoid")
    ])
    model.compile("adam", "binary_crossentropy", ["accuracy"])
    model.fit(X, y, epochs=3, batch_size=32)
    model.save("models/cnn_model.h5")
