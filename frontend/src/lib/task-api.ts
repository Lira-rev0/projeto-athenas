import "server-only";

import type { Task } from "@/lib/tasks";

export async function taskRequest(path = "", init?: RequestInit): Promise<Response> {
  const baseUrl = process.env.API_BASE_URL ?? "http://127.0.0.1:8000";

  return fetch(new URL(`/tasks${path}`, baseUrl), {
    ...init,
    cache: "no-store",
    signal: AbortSignal.timeout(8000),
  });
}

export async function listTasks(): Promise<Task[] | null> {
  try {
    const response = await taskRequest();
    if (!response.ok) return null;
    return (await response.json()) as Task[];
  } catch {
    return null;
  }
}
