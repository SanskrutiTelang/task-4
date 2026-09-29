import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        return None

    return psycopg2.connect(database_url)


@app.route("/")
def home():
    connection = get_db_connection()

    notes = []

    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title, content FROM notes ORDER BY id DESC"
        )
        notes = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (%s, %s)",
            (title, content)
        )

        connection.commit()
        cursor.close()
        connection.close()

    return redirect("/")


@app.route("/health")
def health():
    return "Application is running successfully!"


if __name__ == "__main__":
    app.run(debug=True)