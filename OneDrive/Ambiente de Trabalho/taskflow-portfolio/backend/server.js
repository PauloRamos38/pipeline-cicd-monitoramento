const express = require("express");
const cors = require("cors");
const fs = require("fs/promises");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const DB_PATH = path.join(__dirname, "tasks.json");

app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok", message: "Backend ativo." });
});

async function readTasks() {
  try {
    const data = await fs.readFile(DB_PATH, "utf-8");
    const parsed = JSON.parse(data);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    if (error.code === "ENOENT") {
      await fs.writeFile(DB_PATH, "[]", "utf-8");
      return [];
    }
    throw error;
  }
}

async function writeTasks(tasks) {
  await fs.writeFile(DB_PATH, JSON.stringify(tasks, null, 2), "utf-8");
}

function normalizeNewTask(payload) {
  const title = String(payload.title || "").trim();
  const description = String(payload.description || "").trim();
  const priority = String(payload.priority || "media").toLowerCase();
  const dueDate = String(payload.dueDate || "").trim();

  if (!title) {
    return { error: "Titulo e obrigatorio." };
  }

  const allowedPriorities = ["baixa", "media", "alta"];
  if (!allowedPriorities.includes(priority)) {
    return { error: "Prioridade invalida." };
  }

  const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

  return {
    task: {
      id,
      title,
      description,
      priority,
      dueDate,
      completed: false,
      createdAt: new Date().toISOString()
    }
  };
}

app.get("/tasks", async (req, res) => {
  try {
    const tasks = await readTasks();
    res.json(tasks);
  } catch (error) {
    res.status(500).json({ error: "Erro ao buscar tarefas." });
  }
});

app.post("/tasks", async (req, res) => {
  const { task, error } = normalizeNewTask(req.body || {});
  if (error) {
    return res.status(400).json({ error });
  }

  try {
    const tasks = await readTasks();
    tasks.unshift(task);
    await writeTasks(tasks);
    res.status(201).json(task);
  } catch (err) {
    res.status(500).json({ error: "Erro ao criar tarefa." });
  }
});

app.put("/tasks/reorder", async (req, res) => {
  try {
    const orderedIds = Array.isArray(req.body?.orderedIds) ? req.body.orderedIds : null;

    if (!orderedIds || orderedIds.some((id) => typeof id !== "string")) {
      return res.status(400).json({ error: "Payload de ordenacao invalido." });
    }

    const tasks = await readTasks();

    if (orderedIds.length !== tasks.length) {
      return res.status(400).json({ error: "A lista de ids nao corresponde ao total de tarefas." });
    }

    const taskMap = new Map(tasks.map((task) => [task.id, task]));
    const reordered = orderedIds.map((id) => taskMap.get(id)).filter(Boolean);

    if (reordered.length !== tasks.length) {
      return res.status(400).json({ error: "Ordem contem ids invalidos ou duplicados." });
    }

    await writeTasks(reordered);
    res.json(reordered);
  } catch (error) {
    res.status(500).json({ error: "Erro ao reordenar tarefas." });
  }
});

app.put("/tasks/:id", async (req, res) => {
  try {
    const tasks = await readTasks();
    const index = tasks.findIndex((task) => task.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ error: "Tarefa nao encontrada." });
    }

    const current = tasks[index];
    const next = {
      ...current,
      title: req.body.title !== undefined ? String(req.body.title).trim() || current.title : current.title,
      description: req.body.description !== undefined ? String(req.body.description).trim() : current.description,
      dueDate: req.body.dueDate !== undefined ? String(req.body.dueDate).trim() : current.dueDate,
      completed: req.body.completed !== undefined ? Boolean(req.body.completed) : current.completed
    };

    if (req.body.priority !== undefined) {
      const nextPriority = String(req.body.priority).toLowerCase();
      if (!["baixa", "media", "alta"].includes(nextPriority)) {
        return res.status(400).json({ error: "Prioridade invalida." });
      }
      next.priority = nextPriority;
    }

    tasks[index] = next;
    await writeTasks(tasks);
    res.json(next);
  } catch (error) {
    res.status(500).json({ error: "Erro ao atualizar tarefa." });
  }
});

app.delete("/tasks/:id", async (req, res) => {
  try {
    const tasks = await readTasks();
    const index = tasks.findIndex((task) => task.id === req.params.id);

    if (index === -1) {
      return res.status(404).json({ error: "Tarefa nao encontrada." });
    }

    const [deleted] = tasks.splice(index, 1);
    await writeTasks(tasks);
    res.json(deleted);
  } catch (error) {
    res.status(500).json({ error: "Erro ao deletar tarefa." });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor backend rodando em http://localhost:${PORT}`);
});
