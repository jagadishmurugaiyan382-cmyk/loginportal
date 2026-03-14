from flask import Flask, render_template, request, redirect, session
from db import cursor, conn

app = Flask(__name__)
app.secret_key = "secret123"


# -------- LOGIN --------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        result = cursor.fetchone()

        if result:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid login"

    return render_template("login.html")


# -------- REGISTER --------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?,?)",
            (username, password)
        )

        conn.commit()

        return redirect("/")

    return render_template("register.html")


# -------- DASHBOARD --------

@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template("dashboard.html")

    return redirect("/")


# -------- USERS --------

@app.route("/users")
def users():

    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    return render_template("users.html", users=data)


# -------- DELETE --------

@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect("/users")


# -------- EDIT --------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "UPDATE users SET username=?, password=? WHERE id=?",
            (username, password, id)
        )

        conn.commit()

        return redirect("/users")

    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (id,)
    )

    user = cursor.fetchone()

    return render_template("edit.html", user=user)


# -------- LOGOUT --------

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)