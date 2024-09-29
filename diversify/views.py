"""
auth: AJ Boyd, Joshua Culp (aboyd3@umbc.edu)
date: 9/27/24
desc: stores routes for the website
file: views.py
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import json, csv, yfinance as yf
from .data import load_dataset as ld
from pymongo import MongoClient
import holidays, os
from datetime import datetime, timedelta

views = Blueprint("views", __name__)

# mongodb stuff
uri = "mongodb+srv://diversify:ILoveMongoDB@cluster0.2vecs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['test_stock']
collection = db['stocks']

names, tickers = [], []
s = collection.find({})
for x in s:
    names.append(x['name'])
    tickers.append(x['ticker'])

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@views.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        ticker = request.form["stock-choice"]
        print("help:", ticker)
        input_dates, pred_dates = getDates()
        print(len(input_dates), len(pred_dates))
        writeCSV(ticker, input_dates, pred_dates)
        
        return render_template("predict.html", names=names, tickers=tickers, stock=ticker)
    else:
        return render_template("predict.html", names=names, tickers=tickers)


def getDates():
    start = ld.TODAY
    days = 60
    dates = []
    future = []
    # to get a proper list of stock prices, we must take into account the NYSE is closed weekends and U.S. holidays
    us_holidays = holidays.UnitedStates()
    today = start
    while days > 0:
        today -= timedelta(days=1)
        # check if the day is a weekday and not a holiday
        if today.weekday() < 5 and today not in us_holidays:
            days -= 1
            # print(f"{today.month}/{today.day}/{today.year}")
            dates.append(f"{today.month}/{today.day}/{today.year}")
    tdy = ld.TODAY
    i = 0
    j = 0
    while i < 7:
        current_date = tdy + timedelta(days=j)
        # Check if the current date is a weekday and not a holiday
        if current_date.weekday() < 5 and current_date not in us_holidays:
            future.append(f"{current_date.month}/{current_date.day}/{current_date.year}")
            i += 1
            j += 1
        else:
            j += 1
    
    return dates[::-1], future

def writeCSV(ticker, dates, future, filename="diversify/static/csv/prediction.csv"):
    try:
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            stock = collection.find_one({"ticker": ticker}) #Get stock
            realClosing = json.loads(stock['real_input']) #Retrieve real data and convert to list
            print(len(dates), len(realClosing))
            for date, price in zip(dates, realClosing):
                # for the first 60 days:
                # print date to file
                row = [date, "", "", "", price]
                writer.writerow(row)
                
            #Retrieve predicted data and convert to list
            predictedClosing = json.loads(stock['prediction'])
            #for the 7 predicted days:
            for date, price in zip(future, predictedClosing):
                row = [date, "", "", "", price]
                writer.writerow(row)
    except Exception as e:
        print(f"uh oh {e}")

@views.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@views.route("/educate", methods=["GET", "POST"])
def educate():
    return render_template("educate.html")

@views.route("/educate/resource", methods=["GET", "POST"])
def resource():
    return render_template("resource.html")


@views.route("/about/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")