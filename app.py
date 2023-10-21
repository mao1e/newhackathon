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
    if request.method == "POST":
        coursename = request.form.get("coursename")
        courselist = db.execute ("SELECT * FROM thecourselist")
        # db.execute("CREATE TABLE IF NOT EXISTS mylist (rating FLOAT NOT NULL, professor TEXT NOT NULL, diffculty FLOAT NOT NULL, CRN INTEGER NOT NULL, course TEXT NOT NULL, section TEXT  NOT NULL, day TEXT NOT NULL, starttime INTEGER NOT NULL, endtime INTEGER NOT NULL, location TEXT NOT NULL)")
        # db.execute("INSERT INTO mylist SELECT courselist.rating, courselist.professor, courselist.diffculty, thecourselist.CRN, thecourselist.course, thecourselist.section , thecourselist.day, thecourselist.starttime, thecourselist.endtime, thecourselist.location FROM thecourselist LEFT JOIN courselist ON thecourselist.professor = courselist.professor WHERE course = ?;", coursename)
        alllist = db.execute ("SELECT * FROM thecourselist WHERE course = ?", coursename)            
        return render_template("index.html", courselist = courselist, alllist = alllist)
    else:
         # db.execute("CREATE TABLE courselist (rating FLOAT NOT NULL, professor TEXT NOT NULL, diffculty FLOAT NOT NULL)")
        # db.execute(".import --csv --skip 1 AFAM_F2023_data.csv thecourselist")
        courselist = db.execute ("SELECT * FROM thecourselist")            
        return render_template("first.html", courselist = courselist)
    
@app.route("/third")
def index2():
    # coursename = 'ICS 7'
    # courselist = db.execute ("SELECT * FROM thecourselist")
    # # db.execute("CREATE TABLE IF NOT EXISTS mylist (rating FLOAT NOT NULL, professor TEXT NOT NULL, diffculty FLOAT NOT NULL, CRN INTEGER NOT NULL, course TEXT NOT NULL, section TEXT  NOT NULL, day TEXT NOT NULL, starttime INTEGER NOT NULL, endtime INTEGER NOT NULL, location TEXT NOT NULL)")
    # # db.execute("INSERT INTO mylist SELECT courselist.rating, courselist.professor, courselist.diffculty, thecourselist.CRN, thecourselist.course, thecourselist.section , thecourselist.day, thecourselist.starttime, thecourselist.endtime, thecourselist.location FROM thecourselist LEFT JOIN courselist ON thecourselist.professor = courselist.professor WHERE course = ?;", coursename)
    # alllist = db.execute("SELECT * FROM thecourselist WHERE course = ? AND professor = Nick Chivers", coursename)          
    return render_template("third.html")
        


