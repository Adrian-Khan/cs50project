import os
import ast
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, formatTag

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///courses.db")
# Set the URI for the SQLite database
uri = "sqlite:///courses.db"

# Create an SQL database connection
db = SQL(uri)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/interests", methods=["GET", "POST"])
@login_required
def interests():
    if request.method == "GET":
        # display all interest options from tags table
        alltags = db.execute("SELECT tag_name FROM tags")
        tags = []
        for tag in alltags:
            words = re.findall("[A-Z][^A-Z]*", tag["tag_name"])
            format_tag = " ".join(words)
            tags.append({"original": tag["tag_name"], "formatted": format_tag})

        interests = db.execute(
            "SELECT tag_name FROM tags JOIN user_tags ON tags.tag_id = user_tags.tag_id WHERE user_id = ?",
            session["user_id"],
        )
        user_interests = []
        for interest in interests:
            words = re.findall("[A-Z][^A-Z]*", interest["tag_name"])
            formatted_tag = " ".join(words)
            user_interests.append(
                {"original": interest["tag_name"], "formatted": formatted_tag}
            )

        return render_template(
            "/interests.html", tags=tags, user_interests=user_interests
        )

    elif request.method == "POST":
        selection = request.form.getlist("select")
        deselection = request.form.getlist("deselect")
        if selection:
            for select in selection:
                tagid = db.execute(
                    "SELECT tag_id FROM tags WHERE tag_name = ?", select
                )[0]["tag_id"]
                existing_record = db.execute(
                    "SELECT * FROM user_tags WHERE user_id = ? AND tag_id = ?",
                    session["user_id"],
                    tagid,
                )
                if not existing_record:
                    db.execute(
                        "INSERT INTO user_tags (user_id, tag_id) VALUES (?, ?)",
                        session["user_id"],
                        tagid,
                    )
        if deselection:
            for deselect in deselection:
                deselect_tagid = db.execute(
                    "SELECT tag_id FROM tags WHERE tag_name = ?", deselect
                )[0]["tag_id"]
                print("!!!!!!!!!!", deselect_tagid)
                db.execute(
                    "DELETE FROM user_tags WHERE user_id = ? AND tag_id = ?",
                    session["user_id"],
                    deselect_tagid,
                )
        elif not selection and not deselection:
            return apology(
                "no interests were selected or deselected - feel free to go back to the interets page to select some, or the homepage to see what else you can see on the website.",
                400,
            )
        return redirect("/index")


@app.route("/recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    if request.method == "GET":
        interests = db.execute(
            "SELECT tags.tag_id FROM tags JOIN user_tags ON tags.tag_id = user_tags.tag_id WHERE user_id = ?",
            session["user_id"],
        )  # selects user interests

        courses = []
        for interest in interests:
            course = db.execute(
                "SELECT * FROM courses JOIN course_tags ON courses.course_id = course_tags.course_id WHERE tag_id = ?",
                interest["tag_id"],
            )
            courses.append(course)
        levels = db.execute("SELECT DISTINCT level FROM courses")
        liked_course_id = db.execute(
            "SELECT courses.course_id FROM courses JOIN user_favourite_courses ON courses.course_id = user_favourite_courses.course_id WHERE user_id = ?",
            session["user_id"],
        )

        liked_course_ids = [row["course_id"] for row in liked_course_id]

        return render_template(
            "/recommendations.html",
            courses=courses,
            levels=levels,
            liked_course_id=liked_course_ids,
        )
    elif request.method == "POST":  # filtering
        if request.form.get("selected_level"):
            selected_level = request.form.get("selected_level")
            interests = db.execute(
                "SELECT tags.tag_id FROM tags JOIN user_tags ON tags.tag_id = user_tags.tag_id WHERE user_id = ?",
                session["user_id"],
            )
            levelled_courses = []
            for interest in interests:
                user_level_courses = db.execute(
                    "SELECT * FROM courses JOIN course_tags ON courses.course_id = course_tags.course_id WHERE tag_id = ? AND level = ?",
                    interest["tag_id"],
                    selected_level,
                )
                if user_level_courses:
                    levelled_courses.append(user_level_courses)
            if not levelled_courses:
                no_courses = True  # to pass to the filter to display the error that there are no courses
            else:
                no_courses = False

        liked_course_id = db.execute(
            "SELECT courses.course_id FROM courses JOIN user_favourite_courses ON courses.course_id = user_favourite_courses.course_id WHERE user_id = ?",
            session["user_id"],
        )

        liked_course_ids = [row["course_id"] for row in liked_course_id]

        return render_template(
            "/filtered_recommendations.html",
            levelled_courses=levelled_courses,
            selected_level=selected_level,
            liked_course_id=liked_course_ids,
            no_courses=no_courses,
        )


@app.route("/like_course", methods=["POST"])
def like_course():
    data = request.get_json()
    course_id = data["courseId"]
    is_liked = data["isLiked"]

    # Handle the like/dislike action ie: update a database -  # which table to update????
    existing_record = db.execute(
        "SELECT * FROM user_favourite_courses WHERE user_id = ? AND course_id = ?",
        session["user_id"],
        course_id,
    )
    # test print below
    if is_liked and not existing_record:
        db.execute(
            "INSERT INTO user_favourite_courses (user_id, course_id) VALUES(?,?)",
            session["user_id"],
            course_id,
        )
    elif not is_liked and existing_record:
        db.execute(
            "DELETE FROM user_favourite_courses WHERE user_id =? AND course_id =?",
            session["user_id"],
            course_id,
        )
    # return response to client
    response_data = {"status": "success"}
    return jsonify(response_data)


@app.route("/")
def default_page():
    return redirect("/register")


@app.route("/index", methods=["GET"])
@login_required
def index():
    name = db.execute(
        "SELECT username FROM users where user_id = ?", session["user_id"]
    )[0]["username"]

    interests = db.execute(
        "SELECT tag_name FROM tags JOIN user_tags ON tags.tag_id = user_tags.tag_id WHERE user_id = ?",
        session["user_id"],
    )
    user_interests = []
    for interest in interests:
        words = re.findall("[A-Z][^A-Z]*", interest["tag_name"])
        formatted_tag = " ".join(words)
        user_interests.append(formatted_tag)
    fave_courses = db.execute(
        "SELECT * FROM courses JOIN user_favourite_courses ON courses.course_id = user_favourite_courses.course_id WHERE user_id = ?",
        session["user_id"],
    )
    return render_template(
        "/index.html", name=name, interests=user_interests, fave_courses=fave_courses
    )


# register users
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # user reached route via GET so display registration form
    if request.method == "GET":
        # Forget any user_id
        session.clear()
        return render_template("/register.html")

    elif request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must create username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must create password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        # Query database for username and ensure its unique
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:  # if a row is returned it means the username already exists
            return apology("username already exists", 400)

        # ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Require users’ passwords to have some number of letters, numbers, and/or symbols.
        if not re.match(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            request.form.get("password"),
        ):
            return apology(
                "password must contain at least one letter, number, special character and be 8 characters long",
                400,
            )

        # Add the user's entry into the database
        username = request.form.get("username")
        passwordhash = generate_password_hash(request.form.get("password"))
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)", username, passwordhash
        )

        return redirect("/login")  # confirm entry


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/index")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
