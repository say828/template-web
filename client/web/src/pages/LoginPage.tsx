import { useState } from "react";
import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "@/auth/AuthProvider";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { appTheme } from "@/theme";
import { appThemeVars } from "@/theme-vars";

export function LoginPage() {
  const { authenticating, login, user } = useAuth();
  const location = useLocation();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  if (user) {
    const destination = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? "/";
    return <Navigate to={destination} replace />;
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    try {
      await login({ email, password });
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "로그인에 실패했습니다.");
    }
  }

  return (
    <div className="min-h-screen bg-[var(--app-shell-bg)] px-6 py-12 text-[#22314d]" style={appThemeVars(appTheme)}>
      <div className="mx-auto grid max-w-6xl gap-10 lg:grid-cols-[1.1fr_420px] lg:items-center">
        <div>
          <p className="inline-flex rounded-full bg-white px-4 py-2 text-sm font-semibold text-[#223a82] shadow-sm">Customer workspace</p>
          <h1 className="mt-6 text-5xl font-black tracking-[-0.04em] text-[#16253f]">실제 API에 연결된 로그인 흐름</h1>
          <p className="mt-5 max-w-xl text-lg leading-8 text-[#5f6e86]">
            `VITE_API_BASE_URL/auth/login`으로 인증하고, 저장된 토큰으로 `auth/me`를 다시 호출해 앱 셸을 엽니다.
          </p>
        </div>

        <Card className="border-[var(--app-border)] bg-white p-7 shadow-[0_24px_60px_rgba(31,58,138,0.1)]">
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <p className="text-2xl font-bold text-[#16253f]">Sign in</p>
              <p className="mt-2 text-sm text-[#6b7890]">예시 계정 값이 기본으로 채워져 있습니다.</p>
            </div>

            <label className="block space-y-2">
              <span className="text-sm font-semibold text-[#314157]">Email</span>
              <Input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </label>

            <label className="block space-y-2">
              <span className="text-sm font-semibold text-[#314157]">Password</span>
              <Input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            </label>

            {error ? <p className="text-sm font-medium text-[#c53030]">{error}</p> : null}

            <Button className="w-full" size="lg" type="submit" disabled={authenticating}>
              {authenticating ? "Signing in..." : "Continue to app"}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
