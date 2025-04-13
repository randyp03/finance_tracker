# importing built-in libraries
import csv
from datetime import datetime
import os

# importing flask libraries
from flask import Flask, render_template, request, redirect, url_for, Response

# importing external libraries
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visuals")
def visuals():
    return render_template("visuals.html")

if __name__ == "__main__":
    app.run(debug=True)