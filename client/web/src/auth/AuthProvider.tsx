import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

import { getMe, login as loginRequest } from "@/auth/auth-client";
import type { AuthToken, AuthUser, LoginCommand } from "@/auth/types";

const STORAGE_KEY = "web.auth.token";

interface AuthContextValue {
  user: AuthUser | null;
  token: AuthToken | null;
  initializing: boolean;
  authenticating: boolean;
  login: (command: LoginCommand) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function readStoredToken(): AuthToken | null {
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as AuthToken;
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

function storeToken(token: AuthToken | null) {
  if (token) {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(token));
    return;
  }

  window.localStorage.removeItem(STORAGE_KEY);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<AuthToken | null>(() => readStoredToken());
  const [user, setUser] = useState<AuthUser | null>(null);
  const [initializing, setInitializing] = useState(true);
  const [authenticating, setAuthenticating] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function bootstrap() {
      if (!token) {
        setUser(null);
        setInitializing(false);
        return;
      }

      try {
        const currentUser = await getMe(token.access_token);
        if (!cancelled) {
          setUser(currentUser);
        }
      } catch {
        if (!cancelled) {
          setToken(null);
          setUser(null);
          storeToken(null);
        }
      } finally {
        if (!cancelled) {
          setInitializing(false);
        }
      }
    }

    void bootstrap();

    return () => {
      cancelled = true;
    };
  }, [token]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      initializing,
      authenticating,
      async login(command) {
        setAuthenticating(true);
        try {
          const nextToken = await loginRequest(command);
          storeToken(nextToken);
          setToken(nextToken);
          const currentUser = await getMe(nextToken.access_token);
          setUser(currentUser);
        } finally {
          setAuthenticating(false);
          setInitializing(false);
        }
      },
      logout() {
        storeToken(null);
        setToken(null);
        setUser(null);
        setInitializing(false);
      },
    }),
    [authenticating, initializing, token, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
