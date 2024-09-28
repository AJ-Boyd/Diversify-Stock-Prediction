"""
auth: AJ Boyd
date: 9/27/24
desc: scrapes yahoo finance and stores relevant stock data in mongo database
file: load_dataset.py
"""

import yfinance as yf
import time, holidays, json
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient



# scrapes yahoo finance and stoes info in database
def store_data(ticker):
    try: 
        # get stock info
        stock = yf.Ticker(ticker) 
        name = stock.info['shortName'] 
        inputs = stock.history(start=INPUT_DATE_START, end=INPUT_DATE_END)['Close'].tolist() # get input data
        labels = stock.history(start=LABEL_DATE_START, end=LABEL_DATE_END)['Close'].tolist() # get label data
        
        # convert inputs and labels into json strings
        inputs_str = json.dumps(inputs)
        labels_str = json.dumps(labels)
        
        # store stock info in database
        data = {
            "ticker": ticker,
            "name": name,
            "real_input": inputs_str,
            "real_output": labels_str,
            "norm_input": "[0,0,0]",
            "norm_output": "[0,0,0]",
            "prediction": "[0,0,0]" 
        }
        collection.find_one_and_update(
            {"ticker": ticker},  # Query filter
            {"$setOnInsert": data},  # Insert new data if no document is found
            upsert=True,  # Insert a new document if no match is found
        )
        #collection.insert_one(data)
        
        return True
    except Exception as e:
        print(f"error collecting data for {ticker}: {e}")  
        return False
    
# reads in a file of stock tickers and stores them in a list
def load_tickers(file):
    f = open(file, 'r')
    tickers = f.read().split()
    return tickers

# to ease scraping, we will scrape data in batches
def batch_processing(tickers, batch_size=50, sleep=5):
    print(f"{len(tickers)} stocks to scrape...")
    # i = 0
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        print(f"getting batch from index {i}-{i+batch_size}")
        for ticker in batch:
            if store_data(ticker):
                print(f"stored {ticker}")
                i += 1
                
        print(f"Processed batch {i//batch_size}")
        print('=' * 50)
        time.sleep(sleep)
        
# helper fuunction to subtract weekdays excluding holidays
def subtract_weekdays_excluding_holidays(start, days):
    # to get a proper list of stock prices, we must take into account the NYSE is closed weekends and U.S. holidays
    us_holidays = holidays.UnitedStates()
    today = start
    while days > 0:
        today -= timedelta(days=1)
        # check if the day is a weekday and not a holiday
        if today.weekday() < 5 and today not in us_holidays:
            days -= 1
    return today

# global constants
INPUT_DAYS = 60
OUTPUT_DAYS = 7

# dates for stock scraping
TODAY = datetime.now().date()
INPUT_DATE_START = subtract_weekdays_excluding_holidays(TODAY, INPUT_DAYS + OUTPUT_DAYS) # inclusinve
INPUT_DATE_END = subtract_weekdays_excluding_holidays(TODAY, OUTPUT_DAYS) # non-inclusive
LABEL_DATE_START = INPUT_DATE_END # inclusive
LABEL_DATE_END = subtract_weekdays_excluding_holidays(TODAY, 0) # non-inclusive
print("Input dates:", INPUT_DATE_START, INPUT_DATE_END)
print("Labal dates:", LABEL_DATE_START, LABEL_DATE_END)

uri = "mongodb+srv://diversify:ILoveMongoDB@cluster0.2vecs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['test_stock']
collection = db['stocks']

if __name__ == "__main__":
    try:
        ticker_file = "tickers.txt"
        tickers = load_tickers(ticker_file)
        batch_processing(tickers)
    except Exception as e:
        print(f"error in retrieving tickers: {e}")
    