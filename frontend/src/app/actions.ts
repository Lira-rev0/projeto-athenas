"use server";

import { revalidatePath } from "next/cache";

import { taskRequest } from "@/lib/task-api";
import { taskPriorities, taskStatuses, type TaskActionState } from "@/lib/tasks";

function failure(message: string): TaskActionState {
  return { status: "error", message };
}

function responseError(status: number, fallback: string): TaskActionState {
  if (status === 404) return failure("Esta tarefa não existe mais. Atualize a lista.");
  if (status === 422) return failure("Confira os campos informados e tente novamente.");
  return failure(fallback);
}

export async function createTask(
  _previous: TaskActionState,
  formData: FormData,
): Promise<TaskActionState> {
  const title = String(formData.get("title") ?? "").trim();
  const description = String(formData.get("description") ?? "").trim() || null;
  const priority = String(formData.get("priority") ?? "media");
  // The browser converts its local input to ISO UTC before invoking this action.
  const dueAt = String(formData.get("due_at") ?? "") || null;

  if (!title || title.length > 200) {
    return failure("Informe um título entre 1 e 200 caracteres, além de espaços.");
  }
  if (description && description.length > 5000) {
    return failure("A descrição deve ter no máximo 5.000 caracteres.");
  }
  if (!Object.hasOwn(taskPriorities, priority)) return failure("Selecione uma prioridade válida.");
  if (dueAt && (!/^\d{4}-\d{2}-\d{2}T.+(?:Z|[+-]\d{2}:\d{2})$/.test(dueAt) || Number.isNaN(Date.parse(dueAt)))) {
    return failure("Informe um prazo válido, com fuso horário.");
  }

  try {
    const response = await taskRequest("", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description, priority, due_at: dueAt }),
    });
    if (!response.ok) {
      return responseError(response.status, "Não foi possível criar a tarefa. Tente novamente.");
    }
  } catch {
    return failure("Não foi possível confirmar a criação. Atualize a lista antes de tentar novamente.");
  }

  revalidatePath("/");
  return { status: "success", message: "Tarefa criada com sucesso." };
}

export async function updateTask(
  _previous: TaskActionState,
  formData: FormData,
): Promise<TaskActionState> {
  const id = String(formData.get("task_id") ?? "");
  const operation = String(formData.get("operation") ?? "");
  const status = String(formData.get("status") ?? "");

  if (!/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i.test(id)) {
    return failure("Não foi possível identificar a tarefa. Atualize a lista.");
  }
  if (operation !== "delete" && operation !== "status") return failure("Ação inválida.");
  if (operation === "status" && !Object.hasOwn(taskStatuses, status)) {
    return failure("Selecione um status válido.");
  }

  try {
    const response = await taskRequest(`/${id}`, {
      method: operation === "delete" ? "DELETE" : "PATCH",
      ...(operation === "status" && {
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      }),
    });
    if (!response.ok) {
      return responseError(
        response.status,
        operation === "delete"
          ? "Não foi possível excluir a tarefa. Tente novamente."
          : "Não foi possível atualizar o status. Tente novamente.",
      );
    }
  } catch {
    return failure("Não foi possível confirmar a alteração. Atualize a lista e tente novamente.");
  }

  revalidatePath("/");
  return {
    status: "success",
    message: operation === "delete" ? "Tarefa excluída." : "Status atualizado.",
  };
}
