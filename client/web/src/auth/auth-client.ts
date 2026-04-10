import type { AuthToken, AuthUser, LoginCommand } from "@/auth/types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, "") ?? "";

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

export async function login(command: LoginCommand): Promise<AuthToken> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(command),
  });

  return readJson<AuthToken>(response);
}

export async function getMe(accessToken: string): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  return readJson<AuthUser>(response);
}
