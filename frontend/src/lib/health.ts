export async function isApiHealthy(): Promise<boolean> {
  const baseUrl = process.env.API_BASE_URL ?? "http://127.0.0.1:8000";

  try {
    const response = await fetch(new URL("/health", baseUrl), {
      cache: "no-store",
      signal: AbortSignal.timeout(4000),
    });
    if (!response.ok) return false;

    const body: unknown = await response.json();
    return (
      typeof body === "object" &&
      body !== null &&
      "status" in body &&
      body.status === "ok"
    );
  } catch {
    return false;
  }
}
