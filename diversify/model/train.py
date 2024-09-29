from keras import models 
from pymongo import MongoClient
import json
import numpy as np

# mongodb stuff
uri = "Enter your uri here"
client = MongoClient(uri)
db = client['test_stock']
collection = db['stocks']

# function loads normalized data from db
def get_dataset():
    try:
        inputs, labels = [], []
        
        stocks = collection.find({}) 
        for stock in stocks:
            # gets input and label as a list
            currInput = json.loads(stock["norm_input"])
            currLabel = json.loads(stock["norm_output"])
            inputs.append(currInput)
            labels.append(currLabel)    
        return np.array(inputs), np.array(labels)
    except Exception as e:
        print(f'asdf: {e}')
        return [], []


def train_model(model):
    return model.fit(x_train, y_train, epochs=1000, batch_size=32, validation_split=0.2)

# given entries and their correspoding labels, split between test and training portions on a 20/80
def split_dataset(X, y):
    entries = len(X)
    n_train = int(entries * .8)
    print(f"{n_train} entries for training")
    n_test = entries - n_train
    print(f"{n_test} entries for testing")
    
    x_train = X[:n_train] # first 80% for test
    y_train = y[:n_train]
    x_test = X[n_train:] # remaining 20% for test
    y_test = y[n_train:]
    
    return x_train, x_test, y_train, y_test

if __name__ == "__main__":
    try:
        model = models.load_model('stock_pred_lstm_untrained.keras') # load model
        model.summary()
        model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
        X, y = get_dataset() # load dataset
        x_train, x_test, y_train, y_test = split_dataset(X, y)
        
        history = train_model(model) 
        model.save('stock_pred_lstm_pretrained.keras')
        print("model trained!")
    except Exception as e:
        print(f"uh oh: {e}")
        




