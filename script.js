document.addEventListener("DOMContentLoaded", () => {
    loadTasks();

    
    document.getElementById("filterAll").addEventListener("click", () => filterTasks("all"));
    document.getElementById("filterActive").addEventListener("click", () => filterTasks("active"));
    document.getElementById("filterCompleted").addEventListener("click", () => filterTasks("completed"));
});

function loadTasks() {
    fetch("/tasks")
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";
            tasks.forEach(task => {
                createTaskElement(task);
            });
        });
}

function createTaskElement(task) {
    const taskList = document.getElementById("taskList");

    const li = document.createElement("li");
    li.textContent = task.task;
    if (task.completed) li.classList.add("completed");

    const completeBtn = document.createElement("button");
    completeBtn.textContent = "✔";
    completeBtn.onclick = () => completeTask(task.id);

    const editBtn = document.createElement("button");
    editBtn.textContent = "✏️";
    editBtn.onclick = () => editTask(task);

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "❌";
    deleteBtn.onclick = () => deleteTask(task.id);

    li.appendChild(completeBtn);
    li.appendChild(editBtn);
    li.appendChild(deleteBtn);
    taskList.appendChild(li);
}

function addTask() {
    const taskInput = document.getElementById("taskInput");
    const task = taskInput.value.trim();
    if (task) {
        fetch("/tasks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task })
        }).then(() => {
            taskInput.value = "";
            loadTasks();
        });
    }
}

function completeTask(taskId) {
    fetch(`/tasks/${taskId}`, { method: "PUT" }).then(() => loadTasks());
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, { method: "DELETE" }).then(() => loadTasks());
}

function editTask(task) {
    const newTaskName = prompt("Edit your task:", task.task);
    if (newTaskName !== null && newTaskName.trim() !== "") {
        fetch(`/tasks/${task.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task: newTaskName })
        }).then(() => loadTasks());
    }
}

function filterTasks(filter) {
    fetch("/tasks")
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";

            let filteredTasks = tasks;
            if (filter === "active") {
                filteredTasks = tasks.filter(task => !task.completed);
            } else if (filter === "completed") {
                filteredTasks = tasks.filter(task => task.completed);
            }

            filteredTasks.forEach(task => createTaskElement(task));
        });
}
