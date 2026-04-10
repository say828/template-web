import { Bell, Search } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "@/auth/AuthProvider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { appTheme } from "@/theme";
import { appThemeVars } from "@/theme-vars";

const navItems = [
  { to: "/", label: "Overview" },
  { to: "/orders", label: "Orders" },
];

export function AppShell() {
  const { logout, user } = useAuth();

  return (
    <div className="min-h-screen bg-[var(--app-shell-bg)] text-[#22314d]" style={appThemeVars(appTheme)}>
      <header className="border-b border-[var(--app-border)] bg-white">
        <div className="mx-auto flex max-w-7xl items-center gap-6 px-6 py-4">
          <div className="font-black tracking-[0.18em] text-[#16253f]">PRODUCT</div>
          <nav className="flex items-center gap-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm font-semibold ${isActive ? "bg-[#eef2ff] text-[#223a82]" : "text-[#6b7890]"}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <div className="ml-auto flex items-center gap-3">
            <div className="relative w-[280px]">
              <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8d97a8]" />
              <Input className="pl-9" placeholder="Search workspace" />
            </div>
            <button className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-[var(--app-border)] bg-white">
              <Bell className="h-4 w-4 text-[#5f6e86]" />
            </button>
            <div className="hidden rounded-full bg-[#f7f9fc] px-4 py-2 text-sm font-semibold text-[#314157] md:block">
              {user?.name ?? user?.email}
            </div>
            <Button variant="outline" onClick={logout}>
              Log out
            </Button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-6">
        <Outlet />
      </main>
    </div>
  );
}
