export const taskStatuses = {
  pendente: "Pendente",
  em_andamento: "Em andamento",
  concluida: "Concluída",
  cancelada: "Cancelada",
} as const;

export const taskPriorities = {
  baixa: "Baixa",
  media: "Média",
  alta: "Alta",
  urgente: "Urgente",
} as const;

export type TaskStatus = keyof typeof taskStatuses;
export type TaskPriority = keyof typeof taskPriorities;

export type Task = {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  due_at: string | null;
  created_at: string;
  updated_at: string;
};

export type TaskActionState = {
  status: "idle" | "success" | "error";
  message: string;
};

export const initialActionState: TaskActionState = { status: "idle", message: "" };
