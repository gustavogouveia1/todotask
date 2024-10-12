document.addEventListener('DOMContentLoaded', function() {
    loadTasks();

    function loadTasks() {
        fetch('http://127.0.0.1:5000/tasks')
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';  // Limpa a lista antes de adicionar as novas tarefas

            const sortedTasks = data.tasks.sort((a, b) => {
                const statusOrder = {
                    'em andamento': 1,
                    'pendente': 2,
                    'completa': 3
                };
                return statusOrder[a.status] - statusOrder[b.status];
            });

            // Adiciona cada tarefa à lista
            sortedTasks.forEach(task => {
                addTaskToList(task);
            });
        })
        .catch(err => {
            console.error("Erro ao carregar as tarefas:", err);
        });
    }

    function addTaskToList(task) {
        const taskList = document.getElementById('task-list');
        const li = document.createElement('li');
        li.className = task.status === 'completa' ? 'completed' : '';
        li.setAttribute('data-id', task.id);

        const span = document.createElement('span');
        span.textContent = task.title;

        li.appendChild(span);
        taskList.appendChild(li);
    }
});
