from flask import Flask, redirect, render_template, session

from db import cursor,conn

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------- LOGIN ----------------

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


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db.cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s,%s)",
            (username, password)
        )

        db.conn.commit()

        return redirect("/")

    return render_template("register.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template("dashboard.html")

    return redirect("/")
@app.route("/users")
def users():

    db.cursor.execute("SELECT * FROM users")

    data = db.cursor.fetchall()

    return render_template("users.html", users=data)

@app.route("/delete/<int:id>")
def delete(id):

    db.cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    db.conn.commit()

    return redirect("/users")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db.cursor.execute(
            "UPDATE users SET username=%s, password=%s WHERE id=%s",
            (username, password, id)
        )

        db.conn.commit()

        return redirect("/users")

    db.cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (id,)
    )

    user = db.cursor.fetchone()

    return render_template("edit.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)