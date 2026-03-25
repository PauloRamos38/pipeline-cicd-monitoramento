const API_URL = "http://localhost:3000/tasks";

const state = {
  tasks: [],
  filter: "all",
  search: ""
};

const form = document.getElementById("taskForm");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const priorityInput = document.getElementById("priority");
const dueDateInput = document.getElementById("dueDate");
const taskList = document.getElementById("taskList");
const emptyState = document.getElementById("emptyState");
const feedback = document.getElementById("formFeedback");
const searchInput = document.getElementById("searchInput");
const filterButtons = Array.from(document.querySelectorAll(".filter-btn"));
const pendingCount = document.getElementById("pendingCount");
const themeToggle = document.getElementById("themeToggle");
const exportBtn = document.getElementById("exportBtn");
let draggedTaskId = null;

function setTheme(mode) {
  document.body.classList.toggle("dark", mode === "dark");
  localStorage.setItem("taskflow-theme", mode);

  const icon = themeToggle.querySelector("i");
  const label = themeToggle.querySelector("span");

  if (mode === "dark") {
    icon.className = "fa-solid fa-sun";
    label.textContent = "Modo claro";
  } else {
    icon.className = "fa-solid fa-moon";
    label.textContent = "Modo escuro";
  }
}

function initTheme() {
  const persisted = localStorage.getItem("taskflow-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(persisted || (prefersDark ? "dark" : "light"));
}

function formatDate(value) {
  if (!value) return "Sem data";
  const date = new Date(value + "T00:00:00");
  if (Number.isNaN(date.getTime())) return "Sem data";
  return date.toLocaleDateString("pt-BR");
}

function mapPriority(priority) {
  if (priority === "alta") return { label: "Alta", className: "high" };
  if (priority === "baixa") return { label: "Baixa", className: "low" };
  return { label: "Media", className: "medium" };
}

function getVisibleTasks() {
  return state.tasks.filter((task) => {
    const matchesFilter =
      state.filter === "all" ||
      (state.filter === "pending" && !task.completed) ||
      (state.filter === "done" && task.completed);

    const matchesSearch = task.title
      .toLowerCase()
      .includes(state.search.toLowerCase());

    return matchesFilter && matchesSearch;
  });
}

function updateCounters() {
  const pending = state.tasks.filter((task) => !task.completed).length;
  pendingCount.textContent = String(pending);
}

function taskTemplate(task) {
  const priorityMeta = mapPriority(task.priority);

  return `
    <li class="task-card ${task.completed ? "done" : ""}" data-id="${task.id}" draggable="true">
      <div class="task-head">
        <div>
          <h4 class="task-title">${task.title}</h4>
          <p class="task-desc">${task.description || "Sem descricao"}</p>
        </div>
      </div>
      <div class="task-meta">
        <span class="badge ${priorityMeta.className}">${priorityMeta.label}</span>
        <span><i class="fa-regular fa-calendar"></i> ${formatDate(task.dueDate)}</span>
      </div>
      <div class="task-actions">
        <button class="icon-btn" data-action="toggle" type="button" aria-label="Alternar concluida">
          <i class="fa-solid ${task.completed ? "fa-rotate-left" : "fa-check"}"></i>
          ${task.completed ? "Reabrir" : "Concluir"}
        </button>
        <button class="icon-btn danger" data-action="delete" type="button" aria-label="Excluir tarefa">
          <i class="fa-solid fa-trash"></i>
          Excluir
        </button>
      </div>
    </li>
  `;
}

function renderTasks() {
  const visibleTasks = getVisibleTasks();
  taskList.innerHTML = visibleTasks.map(taskTemplate).join("");
  emptyState.style.display = visibleTasks.length ? "none" : "block";
  updateCounters();
}

async function loadTasks() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error("Falha ao carregar tarefas.");
    }
    state.tasks = await response.json();
    renderTasks();
  } catch (error) {
    feedback.textContent = "Nao foi possivel conectar ao backend na porta 3000.";
  }
}

async function createTask(payload) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Erro ao criar tarefa.");
  }

  return data;
}

async function updateTask(id, payload) {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.error || "Erro ao atualizar tarefa.");
  }

  return response.json();
}

async function deleteTask(id) {
  const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.error || "Erro ao excluir tarefa.");
  }
}

async function reorderTasks(orderedIds) {
  const response = await fetch(`${API_URL}/reorder`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ orderedIds })
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.error || "Erro ao salvar ordem das tarefas.");
  }

  return response.json();
}

function clearDropTargets() {
  document.querySelectorAll(".task-card.drop-target").forEach((card) => {
    card.classList.remove("drop-target");
  });
}

function moveTaskInState(sourceId, targetId) {
  const sourceIndex = state.tasks.findIndex((task) => task.id === sourceId);
  const targetIndex = state.tasks.findIndex((task) => task.id === targetId);

  if (sourceIndex === -1 || targetIndex === -1 || sourceIndex === targetIndex) {
    return false;
  }

  const [moved] = state.tasks.splice(sourceIndex, 1);
  state.tasks.splice(targetIndex, 0, moved);
  return true;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.textContent = "";

  const title = titleInput.value.trim();
  if (!title) {
    feedback.textContent = "Informe um titulo para a tarefa.";
    titleInput.focus();
    return;
  }

  const payload = {
    title,
    description: descriptionInput.value.trim(),
    priority: priorityInput.value,
    dueDate: dueDateInput.value
  };

  try {
    const created = await createTask(payload);
    state.tasks.unshift(created);
    renderTasks();
    form.reset();
    priorityInput.value = "media";
  } catch (error) {
    feedback.textContent = error.message;
  }
});

taskList.addEventListener("click", async (event) => {
  const target = event.target.closest("button[data-action]");
  if (!target) return;

  const card = target.closest(".task-card");
  const taskId = card?.dataset.id;
  if (!taskId) return;

  const task = state.tasks.find((item) => item.id === taskId);
  if (!task) return;

  const action = target.dataset.action;

  try {
    if (action === "toggle") {
      const updated = await updateTask(taskId, { completed: !task.completed });
      state.tasks = state.tasks.map((item) => (item.id === taskId ? updated : item));
      renderTasks();
    }

    if (action === "delete") {
      card.classList.add("removing");
      await new Promise((resolve) => setTimeout(resolve, 190));
      await deleteTask(taskId);
      state.tasks = state.tasks.filter((item) => item.id !== taskId);
      renderTasks();
    }
  } catch (error) {
    feedback.textContent = error.message;
  }
});

taskList.addEventListener("dragstart", (event) => {
  const card = event.target.closest(".task-card");
  if (!card || state.filter !== "all" || state.search) {
    event.preventDefault();
    return;
  }

  draggedTaskId = card.dataset.id;
  card.classList.add("dragging");

  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", draggedTaskId);
  }
});

taskList.addEventListener("dragover", (event) => {
  if (!draggedTaskId) return;
  event.preventDefault();

  const card = event.target.closest(".task-card");
  clearDropTargets();

  if (card && card.dataset.id !== draggedTaskId) {
    card.classList.add("drop-target");
  }
});

taskList.addEventListener("dragleave", (event) => {
  const card = event.target.closest(".task-card");
  if (card) {
    card.classList.remove("drop-target");
  }
});

taskList.addEventListener("drop", async (event) => {
  event.preventDefault();

  const targetCard = event.target.closest(".task-card");
  const targetId = targetCard?.dataset.id;
  const sourceId = draggedTaskId;

  clearDropTargets();

  if (!sourceId || !targetId || sourceId === targetId) {
    return;
  }

  const snapshot = [...state.tasks];
  const moved = moveTaskInState(sourceId, targetId);
  if (!moved) {
    return;
  }

  renderTasks();

  try {
    await reorderTasks(state.tasks.map((task) => task.id));
  } catch (error) {
    state.tasks = snapshot;
    renderTasks();
    feedback.textContent = error.message;
  }
});

taskList.addEventListener("dragend", (event) => {
  const card = event.target.closest(".task-card");
  if (card) {
    card.classList.remove("dragging");
  }
  draggedTaskId = null;
  clearDropTargets();
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    state.filter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderTasks();
  });
});

searchInput.addEventListener("input", () => {
  state.search = searchInput.value.trim();
  renderTasks();
});

themeToggle.addEventListener("click", () => {
  const isDark = document.body.classList.contains("dark");
  setTheme(isDark ? "light" : "dark");
});

exportBtn.addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(state.tasks, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `taskflow-export-${new Date().toISOString().slice(0, 10)}.json`;
  anchor.click();

  URL.revokeObjectURL(url);
});

initTheme();
loadTasks();
