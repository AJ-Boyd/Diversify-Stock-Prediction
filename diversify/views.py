"""
auth: AJ Boyd (aboyd3@umbc.edu)
date: 9/27/24
desc: stores routes for the website
file: views.py
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")