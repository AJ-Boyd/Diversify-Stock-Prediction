import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tensorflow as tf
from keras import models, layers, Input
from data import load_dataset as ld

# model architecture
if __name__ == "__main__":
    model = models.Sequential()
    model.add(Input(shape=(ld.INPUT_DAYS,1))) # input layer
    model.add(layers.LSTM(128, return_sequences=True))
    model.add(layers.Dropout(0.25))
    model.add(layers.LSTM(64, return_sequences=False))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(0.35))
    model.add(layers.Dense(ld.OUTPUT_DAYS)) # output layer
    model.save('stock_pred_lstm_untrained.keras') # save model
    print("Done!")