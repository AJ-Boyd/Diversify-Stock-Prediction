from keras import models 
from pymongo import MongoClient
import json
import numpy as np
from train import get_dataset, split_dataset
from sklearn.preprocessing import MinMaxScaler


# mongodb stuff
uri = "Enter your uri here"
client = MongoClient(uri)
db = client['test_stock']
collection = db['stocks']

# once a day, predict the next 7 days worth of stock prices and store in database
def predict(model):
    all_stocks = collection.find({})
    
    try:
        for stock in all_stocks:
            pred_input = np.array(json.loads(stock['real_input'])).reshape(1, 60, 1)
            scaled_pred = model.predict(pred_input)
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaler.fit(np.array(json.loads(stock["real_input"])).reshape(-1,1))
            pred = scaler.inverse_transform(scaled_pred)
            p = pred.flatten().tolist()
            
            print(pred.flatten().tolist())
            
            # store pred in database
            collection.update_one({"_id":stock["_id"]}, {"$set": {"prediction":json.dumps(p)}})
            
    except Exception as e:
        print(f"uh oh: {e}")
def test_stock(entry):
    pass

if __name__ == "__main__":
    # X, y = get_dataset()
    # x_train, x_test, y_train, y_test = split_dataset(X, y)
    # x_test = x_test.tolist()
    # test_input = x_test[0]
    # entry = collection.find_one({'norm_input': json.dumps(test_input)})
    # print(f"testing stock: {entry['ticker']}")
    
    model = models.load_model('stock_pred_lstm_pretrained.keras') # load model  
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    
    try:
        predict(model)
        # h = np.array(json.loads(entry['real_input'])).reshape(1, 60, 1)
        # print(len(h))
        # pred = model.predict(h)
        # scaler = MinMaxScaler(feature_range=(0, 1))
        # scaler.fit(np.array(json.loads(entry["real_input"])).reshape(-1,1))
        # q = scaler.inverse_transform(pred)
        # print(q)
        # print(entry['real_output'])
    except Exception as e:
        print(f"error: {e}")

