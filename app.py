import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///rmp.db")


@app.route("/", methods=["GET", "POST"])
def index():
        db.execute("CREATE TABLE courselist (rating FLOAT NOT NULL, professor TEXT NOT NULL, diffculty FLOAT NOT NULL)")
        db.execute(".import --csv --skip 1 products.csv courselist")
        courselist = db.execute ("SELECT * FROM courselist")
        return render_template("index.html", courselist = courselist)


