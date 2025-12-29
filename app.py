from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "tutien_secret_123"

# ===== DATABASE =====
def get_db():
    return sqlite3.connect("game.db")

def init_db():
    db = get_db()
    c = db.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER,
            linh_luc INTEGER,
            canh_gioi TEXT
        )
    """)
    db.commit()

init_db()

# ===== ĐĂNG KÝ =====
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["user"]
        pw = request.form["pw"]

        db = get_db()
        c = db.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (user, pw))
            uid = c.lastrowid
            c.execute("INSERT INTO players VALUES (?,?,?)", (uid, 0, "Luyện Khí"))
            db.commit()
            return redirect("/")
        except:
            return "❌ Tài khoản đã tồn tại"

    return render_template("register.html")

# ===== ĐĂNG NHẬP =====
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pw = request.form["pw"]

        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (user, pw))
        u = c.fetchone()

        if u:
            session["uid"] = u[0]
            return redirect("/game")
        else:
            return "❌ Sai tài khoản hoặc mật khẩu"

    return render_template("login.html")

# ===== GAME =====
@app.route("/game", methods=["GET", "POST"])
def game():
    if "uid" not in session:
        return redirect("/")

    db = get_db()
    c = db.cursor()

    if request.method == "POST":
        tang = random.randint(5, 15)
        c.execute("UPDATE players SET linh_luc = linh_luc + ? WHERE user_id=?", (tang, session["uid"]))
        db.commit()

    c.execute("SELECT linh_luc, canh_gioi FROM players WHERE user_id=?", (session["uid"],))
    p = c.fetchone()

    return render_template("game.html", linh_luc=p[0], canh_gioi=p[1])

app.run()
