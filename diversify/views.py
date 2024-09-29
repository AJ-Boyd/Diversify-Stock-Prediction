"""
auth: AJ Boyd, Joshua Culp (aboyd3@umbc.edu)
date: 9/27/24
desc: stores routes for the website
file: views.py
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from pymongo import MongoClient
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@views.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        ticker = request.form["stock-choice"]
        print("help:", stck)
        
        return render_template("predict.html", names=["Microsoft", "Apple", "Google", "3M"], tickers=["MFST","AAPL","GOOGL","MMM"], stock=stck)
    else:
        return render_template("predict.html", names=["Microsoft", "Apple", "Google", "3M"], tickers=["MFST","AAPL","GOOGL","MMM"])

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