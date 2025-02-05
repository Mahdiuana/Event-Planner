Event Planner
A simple event planner web application built with Flask and SQLite. This app allows you to manage tasks, mark them as completed, edit, and delete tasks, as well as view and filter tasks based on their completion status.

Features
Add tasks: Add tasks to your event plan.
View tasks: View all tasks or filter them based on their completion status.
Edit tasks: Edit the task description.
Complete tasks: Mark tasks as completed.
Delete tasks: Delete individual tasks or delete all tasks at once.
Tech Stack
Backend: Flask (Python web framework)
Database: SQLite (lightweight relational database)
Frontend: HTML, CSS, JavaScript (using Axios for API requests)
Installation
Prerequisites
Python 3.x
SQLite (SQLite comes pre-installed with Python, so no additional installation is required)

Install the required dependencies
It's recommended to use a virtual environment. You can create and activate a virtual environment like this:


python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Then, install the required packages:


pip install -r requirements.txt
If you don't have a requirements.txt file, you can create it by running:




pip freeze > requirements.txt
To manually install Flask and other dependencies, use:


pip install Flask
pip install flask-cors  # If you need CORS support
Run the application

python app.py
By default, the app will run at http://127.0.0.1:5000/.

API Endpoints
GET /tasks
Fetch all tasks.

Response:

json

[
  {
    "id": 1,
    "task": "Example task",
    "completed": false,
    "created_at": "2025-02-05T12:34:56"
  },
  ...
]
POST /tasks
Add a new task. You need to send a JSON object with the task field.

Request body:

json

{
  "task": "New task"
}
Response:

json

{
  "message": "Task added"
}
PUT /tasks/<task_id>
Mark a task as completed.

Response:

json

{
  "message": "Task updated"
}
PATCH /tasks/<task_id>
Edit a task. You need to send a JSON object with the task field.

Request body:

json

{
  "task": "Updated task description"
}
Response:

json

{
  "message": "Task updated"
}
DELETE /tasks/<task_id>
Delete a specific task.

Response:

json
{
  "message": "Task deleted"
}
DELETE /tasks
Delete all tasks.

Response:

json

{
  "message": "All tasks deleted"
}
GET /tasks/filter
Filter tasks based on their completion status. Available filters are completed=true, completed=false, and completed=all.

Example Request:

sql
GET /tasks/filter?completed=true
Response:

json

[
  {
    "id": 1,
    "task": "Completed task",
    "completed": true,
    "created_at": "2025-02-04T12:34:56"
  }
]
Frontend
The frontend provides an interface to interact with the app. It includes:

A text input field to add new tasks.
Buttons to mark tasks as completed, edit, or delete them.
Buttons to filter tasks by their completion status.
Folder Structure


/event-planner
    /templates
        index.html  # Main HTML file
    /static
        style.css   # CSS file for styling
    app.py          # Flask backend
    requirements.txt # List of Python dependencies
    README.md       # This file
