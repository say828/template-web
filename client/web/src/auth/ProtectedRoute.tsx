import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "@/auth/AuthProvider";

export function ProtectedRoute() {
  const { initializing, user } = useAuth();
  const location = useLocation();

  if (initializing) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--app-shell-bg)] text-sm font-medium text-[#5f6e86]">
        세션을 확인하는 중입니다.
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}
