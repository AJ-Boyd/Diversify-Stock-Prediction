import json
import load_dataset as ld, numpy as np
from sklearn.preprocessing import MinMaxScaler
from pymongo import MongoClient
from sklearn.preprocessing import normalize

# if for some reason, the data stored in the db is incorrectly stored, interpolate the data
def clean_data(ticker, input_prices, label_prices):
    try:
        if len(input_prices) < ld.INPUT_DAYS:
            n_missing = ld.INPUT_DAYS - len(input_prices)
            print(f"not enough input data for {ticker}. missing {n_missing} days.\ninterpolating data...")
            interp_input = np.interp(np.arange(ld.INPUT_DAYS), 
                                            np.linspace(0, ld.INPUT_DAYS-1, num=len(input_prices)),
                                            np.array(input_prices))
            # overwrite data in mongo db
            collection.update_one({"ticker": ticker}, {"$set": {"real_input": json.dumps(list(interp_input))}})
    except Exception as e:
        print(f"error in ticker {ticker} during input interpolation. {e}")
    
    try:
        if len(label_prices) < ld.OUTPUT_DAYS:
            n_missing = ld.OUTPUT_DAYS - len(input_prices)
            print(f"not enough label data for {ticker}. missing {n_missing} days.\ninterpolating data...")
            interp_label = np.interp(np.arange(ld.INPUT_DAYS), 
                                            np.linspace(0, ld.INPUT_DAYS-1, num=len(input_prices)),
                                            np.array(input_prices))
            # overwrite data in mongo db
            collection.update_one({"ticker": ticker}, {"$set": {"real_output": json.dumps(list(interp_label))}})
    except Exception as e:
        print(f"error in ticker {ticker} during label interpolation. {e}")
        
# to increase accuracy, let's normalize our data and store them in the database
def normalize_data(ticker, input_prices, label_prices):
    input_prices = np.array(input_prices).reshape(-1,1)
    label_prices = np.array(label_prices).reshape(-1,1)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_inputs = scaler.fit_transform(input_prices).flatten().tolist()
    scaled_labels = scaler.fit_transform(label_prices).flatten().tolist()
    
    # store in database
    scaled_input_str = json.dumps(scaled_inputs)
    scaled_label_str = json.dumps(scaled_labels)
    
    collection.update_one({"ticker": ticker}, {"$set": {"norm_input": scaled_input_str}})
    collection.update_one({"ticker": ticker}, {"$set": {"norm_output": scaled_label_str}})

# connect to database
uri = "mongodb+srv://diversify:ILoveMongoDB@cluster0.2vecs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['test_stock']
collection = db['stocks']

if __name__ == "__main__" :
    # grab all input and label prices
    stocks = collection.find({}) 
    for stock in stocks:
        # gets input and label as a list
        input = json.loads(stock["real_input"])
        label = json.loads(stock["real_output"])
        # clean data
        clean_data(stock["ticker"], input, label)
        # normalize data
        normalize_data(stock["ticker"], input, label)
    
