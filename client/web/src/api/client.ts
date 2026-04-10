const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") ?? "";

interface RequestOptions {
  accessToken?: string;
}

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = (await response.json()) as { detail?: string };
      if (typeof data.detail === "string" && data.detail.length > 0) {
        message = data.detail;
      }
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return (await response.json()) as T;
}

export async function apiGet<T>(path: string, options?: RequestOptions): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: options?.accessToken ? { Authorization: `Bearer ${options.accessToken}` } : undefined,
  });

  return readJson<T>(response);
}
