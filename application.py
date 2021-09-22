import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        message = ""
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        if not name:
            message = "Missing name"
        elif not month:
            message = "Missing month"
        elif not day:
            message = "Missing day"
        else:
            db.execute(
                "INSERT INTO birthdays (name, month, day) VALUES(?, ?,?)",
                name,
                month,
                day,
            )
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message=message, birthdays=birthdays)
    else:
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

@app.route("/edit", methods = ["GET", "POST"])
def edit():

    if request.method == "GET":
        id = request.args.get("id")
        birthday = db.execute("SELECT * FROM birthdays WHERE id = ?", id)
        return render_template("edit.html", birthday=birthday, id=id)
    elif request.method == "POST":
        message1 = ""
        name = request.form["name"]
        month = request.form["month"]
        day = request.form["day"]
        id = request.form["id"]
        birthday = db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id =?", name, month, day, id)
        message1 = "Birthdate Updated Successfully"
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message1=message1, birthdays=birthdays)

@app.route("/delete", methods = ["GET", "POST"])
def delete():

    if request.method == "GET":
        id = request.args.get("id")
        birthday = db.execute("SELECT * FROM birthdays WHERE id = ?", id)
        return render_template("delete.html", birthday=birthday, id=id)
    elif request.method == "POST":
        message1 = ""
        id = request.form["id"]
        birthday = db.execute("DELETE FROM birthdays WHERE id =?", id)
        message1 = "Birthdate Deleted Successfully"
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", message1=message1, birthdays=birthdays)
