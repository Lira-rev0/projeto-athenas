"use client";

import { useActionState, useState, useSyncExternalStore } from "react";

import { createTask, updateTask } from "@/app/actions";
import {
  initialActionState,
  taskPriorities,
  taskStatuses,
  type Task,
  type TaskActionState,
} from "@/lib/tasks";

const emptyFields = { title: "", description: "", priority: "media", due_local: "" };
const subscribeToClient = () => () => {};

function Deadline({ value }: { value: string }) {
  const isClient = useSyncExternalStore(subscribeToClient, () => true, () => false);
  const formatted = new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
    ...(!isClient && { timeZone: "UTC" }),
  }).format(new Date(value));

  return <time dateTime={value}>{formatted}{!isClient && " UTC"}</time>;
}

function ActionFeedback({ state }: { state: TaskActionState }) {
  return (
    <p className={`feedback ${state.status}`} role="status" aria-live="polite">
      {state.message}
    </p>
  );
}

export function CreateTaskForm() {
  const [fields, setFields] = useState(emptyFields);
  const [state, formAction, pending] = useActionState(
    async (previous: TaskActionState, data: FormData): Promise<TaskActionState> => {
      const localDue = String(data.get("due_local") ?? "");
      if (localDue && Number.isNaN(new Date(localDue).getTime())) {
        return { status: "error", message: "Informe um prazo válido." };
      }
      data.set("due_at", localDue ? new Date(localDue).toISOString() : "");
      data.delete("due_local");
      const result = await createTask(previous, data);
      if (result.status === "success") setFields(emptyFields);
      return result;
    },
    initialActionState,
  );

  return (
    <section className="create-panel" aria-labelledby="create-title">
      <p className="eyebrow">UM PASSO DE CADA VEZ</p>
      <h2 id="create-title">Nova tarefa</h2>
      <p className="panel-description">Registre o que precisa da sua atenção.</p>
      <form action={formAction} aria-busy={pending}>
        <fieldset disabled={pending}>
          <label htmlFor="title">Título <span className="required">*</span></label>
          <input id="title" name="title" required maxLength={200} placeholder="O que precisa ser feito?" value={fields.title} onChange={(event) => setFields({ ...fields, title: event.target.value })} />

          <label htmlFor="description">Descrição <span className="optional">opcional</span></label>
          <textarea id="description" name="description" maxLength={5000} rows={3} placeholder="Adicione um pouco de contexto…" value={fields.description} onChange={(event) => setFields({ ...fields, description: event.target.value })} />

          <label htmlFor="priority">Prioridade</label>
          <select id="priority" name="priority" value={fields.priority} onChange={(event) => setFields({ ...fields, priority: event.target.value })}>
            {Object.entries(taskPriorities).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>

          <label htmlFor="due_local">Prazo <span className="optional">opcional</span></label>
          <input id="due_local" name="due_local" type="datetime-local" aria-describedby="deadline-hint" value={fields.due_local} onChange={(event) => setFields({ ...fields, due_local: event.target.value })} />
          <p id="deadline-hint" className="field-hint">Data e hora no fuso do seu dispositivo.</p>

          <button className="primary-button" type="submit">{pending ? "Criando tarefa…" : "Criar tarefa"}<span aria-hidden="true">+</span></button>
        </fieldset>
        <ActionFeedback state={pending ? { status: "idle", message: "Salvando sua tarefa…" } : state} />
      </form>
    </section>
  );
}

export function TaskList({ tasks }: { tasks: Task[] | null }) {
  const [state, formAction, pending] = useActionState(updateTask, initialActionState);

  return (
    <section className="tasks-panel" aria-labelledby="tasks-title" aria-busy={pending}>
      <div className="panel-heading">
        <div>
          <p className="eyebrow">VISÃO GERAL</p>
          <h2 id="tasks-title">Suas tarefas {tasks && <span className="task-count">{tasks.length}</span>}</h2>
        </div>
        <form action="/" method="get">
          <button className="text-link" type="submit">Atualizar lista <span aria-hidden="true">↗</span></button>
        </form>
      </div>
      <p className="panel-description">As mais recentes aparecem primeiro.</p>
      <ActionFeedback state={pending ? { status: "idle", message: "Salvando alteração…" } : state} />

      {tasks === null ? (
        <div className="empty-state error-state" role="alert">
          <span className="empty-mark" aria-hidden="true">!</span>
          <h3>Não foi possível carregar as tarefas.</h3>
          <p>Verifique se os serviços estão disponíveis e tente atualizar a lista.</p>
        </div>
      ) : tasks.length === 0 ? (
        <div className="empty-state">
          <span className="empty-mark" aria-hidden="true">✓</span>
          <h3>Espaço para o que vem a seguir.</h3>
          <p>Crie sua primeira tarefa para organizar os próximos passos.</p>
        </div>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <li className={`task-card task-${task.status}`} key={task.id}>
              <div className="task-badges">
                <span className={`badge status-${task.status}`}>{taskStatuses[task.status]}</span>
                <span className={`priority priority-${task.priority}`}><span className="priority-dot" aria-hidden="true" />{taskPriorities[task.priority]}</span>
              </div>
              <h3>{task.title}</h3>
              {task.description && <p className="task-description">{task.description}</p>}
              {task.due_at && <p className="task-deadline">Prazo <Deadline value={task.due_at} /></p>}
              <div className="task-actions">
                <form action={formAction}>
                  <input type="hidden" name="task_id" value={task.id} />
                  <input type="hidden" name="operation" value="status" />
                  <select key={task.status} aria-label={`Status de ${task.title}`} name="status" defaultValue={task.status} disabled={pending}>
                    {Object.entries(taskStatuses).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                  </select>
                  <button type="submit" disabled={pending}>Salvar status</button>
                </form>
                <form action={formAction} onSubmit={(event) => {
                  if (!window.confirm(`Excluir a tarefa “${task.title}”? Esta ação não pode ser desfeita.`)) event.preventDefault();
                }}>
                  <input type="hidden" name="task_id" value={task.id} />
                  <input type="hidden" name="operation" value="delete" />
                  <button className="delete-button" type="submit" disabled={pending} aria-label={`Excluir tarefa ${task.title}`}>Excluir</button>
                </form>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
