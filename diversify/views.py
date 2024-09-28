"""
auth: AJ Boyd, Joshua Culp (aboyd3@umbc.edu)
date: 9/27/24
desc: stores routes for the website
file: views.py
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@views.route("/predict", methods=["GET", "POST"])
def predict():
    return render_template("predict.html")

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