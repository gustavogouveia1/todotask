document.addEventListener("DOMContentLoaded", function () {
  loadTasks();

  // Carregar tarefas
  function loadTasks() {
    fetch("http://127.0.0.1:5000/tasks")
      .then((response) => response.json())
      .then((data) => {
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = ""; // Limpa a lista antes de adicionar as novas tarefas

        const sortedTasks = data.tasks.sort((a, b) => {
          const statusOrder = {
            "em andamento": 1,
            pendente: 2,
            completa: 3,
          };
          return statusOrder[a.status] - statusOrder[b.status];
        });

        // Adiciona cada tarefa à lista
        sortedTasks.forEach((task) => {
          addTaskToList(task);
        });
      })
      .catch((err) => {
        console.error("Erro ao carregar as tarefas:", err);
      });
  }

  // Adicionar tarefa
  document
    .getElementById("add-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      const taskTitle = document.getElementById("new-task").value.trim();

      // Verificações
      const isNumeric = /^\d+$/.test(taskTitle);
      if (isNumeric) {
        alert("O título da tarefa não pode ser apenas numérico.");
        return;
      }

      if (taskTitle.length < 4) {
        alert("O título da tarefa deve ter pelo menos 4 caracteres.");
        return;
      }

      if (taskTitle) {
        fetch("http://127.0.0.1:5000/tasks/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ todo: taskTitle }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // Atualizar a lista de tarefas
              loadTasks();
            } else {
              alert("Erro ao adicionar tarefa.");
            }
          })
          .catch((err) => {
            alert("Erro ao conectar-se com o servidor.");
            console.error(err);
          });
      } else {
        alert("O título da tarefa não pode estar vazio");
      }
    });

  // Adicionar tarefa à lista no DOM
  function addTaskToList(task) {
    const taskList = document.getElementById("task-list");
    const li = document.createElement("li");
    li.className = task.status === "completa" ? "completed" : "";
    li.setAttribute("data-id", task.id);

    const select = document.createElement("select");
    select.className = "status-select";
    ["pendente", "em andamento", "completa"].forEach((status) => {
      const option = document.createElement("option");
      option.value = status;
      option.text = status.charAt(0).toUpperCase() + status.slice(1);
      if (task.status === status) {
        option.selected = true;
      }
      select.appendChild(option);
    });
    select.addEventListener("change", function () {
      updateTaskStatus(task.id, select.value);
    });

    const span = document.createElement("span");
    span.textContent = task.title;

    if (task.status === "completa") {
      const checkmark = document.createElement("span");
      checkmark.className = "checkmark";
    }

    const editLink = document.createElement("a");
    editLink.href = "#";
    editLink.className = "edit-link";
    editLink.innerHTML = '<i class="fas fa-pencil-alt"></i>'; // Ícone de lápis
    editLink.addEventListener("click", function (event) {
      event.preventDefault();
      editTask(task.id);
    });

    const deleteLink = document.createElement("a");
    deleteLink.href = "#";
    deleteLink.className = "delete-link";
    deleteLink.innerHTML = '<i class="fas fa-trash"></i>'; // Ícone de lixeira
    deleteLink.addEventListener("click", function (event) {
      event.preventDefault();
      deleteTask(task.id);
    });

    li.appendChild(select);
    li.appendChild(span);
    li.appendChild(editLink);
    li.appendChild(deleteLink);
    taskList.appendChild(li);
  }

  // Atualizar status da tarefa
  function updateTaskStatus(taskId, status) {
    fetch(`http://127.0.0.1:5000/tasks/update_status/${taskId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: status }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Recarregar as tarefas para atualizar a ordem
          loadTasks();
        } else {
          alert("Erro ao atualizar status da tarefa.");
        }
      });
  }

  // Deletar tarefa
  function deleteTask(taskId) {
    fetch(`http://127.0.0.1:5000/tasks/delete/${taskId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.querySelector(`li[data-id="${taskId}"]`).remove();
        } else {
          alert("Erro ao deletar tarefa.");
        }
      });
  }
});
