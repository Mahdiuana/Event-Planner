from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            tasks = [
                {"id": row[0], "task": row[1], "completed": bool(row[2]), "created_at": row[3]}
                for row in cursor.fetchall()
            ]
        return jsonify(tasks)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task_text = data.get("task", "").strip()  
    if task_text:  
        try:
            with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task_text,))
                conn.commit()
            return jsonify({"message": "Task added"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
    return jsonify({"error": "Invalid input, task text is required"}), 400


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Task not found"}), 404
        return jsonify({"message": "Task updated"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def edit_task(task_id):
    data = request.json
    new_task_text = data.get("task", "").strip()
    if new_task_text:
        try:
            with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task_text, task_id))
                conn.commit()
                if cursor.rowcount == 0:
                    return jsonify({"error": "Task not found"}), 404
            return jsonify({"message": "Task updated"}), 200
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {e}"}), 500
    return jsonify({"error": "Invalid input, task text is required"}), 400


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({"error": "Task not found"}), 404
        return jsonify({"message": "Task deleted"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


@app.route("/tasks", methods=["DELETE"])
def delete_all_tasks():
    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
            conn.commit()
        return jsonify({"message": "All tasks deleted"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


@app.route("/tasks/filter", methods=["GET"])
def filter_tasks():
    status = request.args.get("completed")
    if status not in ['true', 'false', 'all', None]:
        return jsonify({"error": "Invalid filter value, should be 'true', 'false', or 'all'"}), 400

    query = "SELECT * FROM tasks"
    params = []
    if status == 'true':
        query += " WHERE completed = 1"
    elif status == 'false':
        query += " WHERE completed = 0"

    try:
        with sqlite3.connect("tasks.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            tasks = [
                {"id": row[0], "task": row[1], "completed": bool(row[2]), "created_at": row[3]}
                for row in cursor.fetchall()
            ]
        return jsonify(tasks)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
