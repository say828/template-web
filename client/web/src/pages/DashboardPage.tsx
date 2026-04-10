import { useEffect, useState } from "react";

import { useAuth } from "@/auth/AuthProvider";
import { fetchOrderOverview, type OrderOverviewResponse } from "@/api/orders";
import { Card } from "@/components/ui/card";

export function DashboardPage() {
  const { token } = useAuth();
  const [overview, setOverview] = useState<OrderOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token?.access_token) {
      return;
    }

    let cancelled = false;

    setLoading(true);
    setError(null);

    fetchOrderOverview(token.access_token)
      .then((response) => {
        if (!cancelled) {
          setOverview(response);
        }
      })
      .catch((nextError: Error) => {
        if (!cancelled) {
          setError(nextError.message);
          setOverview(null);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token?.access_token]);

  const recentActivity = overview?.recent_activity ?? [];
  const selectedOrder = overview?.selected_order;

  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_var(--app-panel-width)]">
      <div className="space-y-6">
        <section className="grid gap-4 md:grid-cols-3">
          {(overview?.stats ?? []).map((stat) => (
            <Card key={stat.label} className="p-[var(--app-card-padding)]">
              <p className="text-sm text-[var(--app-muted)]">{stat.label}</p>
              <p className={`mt-3 text-3xl font-bold ${stat.tone ?? "text-[#22314d]"}`}>{stat.value}</p>
            </Card>
          ))}
          {loading && !overview ? (
            <Card className="p-[var(--app-card-padding)] md:col-span-3">
              <p className="text-sm text-[var(--app-muted)]">Overview</p>
              <p className="mt-3 text-lg font-semibold text-[#22314d]">Loading dashboard data...</p>
            </Card>
          ) : null}
          {error ? (
            <Card className="p-[var(--app-card-padding)] md:col-span-3">
              <p className="text-sm text-[var(--app-muted)]">Overview</p>
              <p className="mt-3 text-lg font-semibold text-[var(--app-danger)]">{error}</p>
            </Card>
          ) : null}
        </section>

        <Card className="overflow-hidden">
          <div className="p-[var(--app-card-padding)]">
            <h2 className="text-lg font-bold">Recent activity</h2>
          </div>
          <table className="w-full border-collapse text-sm">
            <thead className="bg-[#f8fafe] text-left text-[#516174]">
              <tr>
                {["Order", "Date", "Customer", "Status"].map((cell) => (
                  <th key={cell} className="border-y border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] font-semibold">
                    {cell}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && !recentActivity.length ? (
                <tr>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-muted)]" colSpan={4}>
                    Recent activity is loading.
                  </td>
                </tr>
              ) : null}
              {error ? (
                <tr>
                  <td
                    className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-danger)]"
                    colSpan={4}
                  >
                    {error}
                  </td>
                </tr>
              ) : null}
              {!loading && !error && !recentActivity.length ? (
                <tr>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-muted)]" colSpan={4}>
                    No recent activity found.
                  </td>
                </tr>
              ) : null}
              {recentActivity.map((row) => (
                <tr key={row.order_id}>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-accent)]">
                    {row.order_id}
                  </td>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">{row.date}</td>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">{row.customer}</td>
                  <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">
                    <span className={row.status === "At risk" ? "text-[var(--app-danger)]" : ""}>{row.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <Card className="p-[var(--app-card-padding)]">
        <h2 className="text-lg font-bold">Selected detail</h2>
        {loading && !selectedOrder ? <p className="mt-5 text-sm text-[var(--app-muted)]">Loading selected order...</p> : null}
        {error ? <p className="mt-5 text-sm font-semibold text-[var(--app-danger)]">{error}</p> : null}
        {selectedOrder ? (
          <div className="mt-5 space-y-4 text-sm">
            <div>
              <p className="text-[var(--app-muted)]">Product</p>
              <p className="mt-1 font-semibold">{selectedOrder.product_name}</p>
            </div>
            <div>
              <p className="text-[var(--app-muted)]">Customer</p>
              <p className="mt-1 font-semibold">{selectedOrder.customer_name}</p>
            </div>
            <div>
              <p className="text-[var(--app-muted)]">Status</p>
              <p className={`mt-1 font-semibold ${selectedOrder.status === "At risk" ? "text-[var(--app-danger)]" : "text-[#314157]"}`}>
                {selectedOrder.status}
              </p>
            </div>
            <div>
              <p className="text-[var(--app-muted)]">Amount</p>
              <p className="mt-1 font-semibold">{selectedOrder.amount}</p>
            </div>
          </div>
        ) : null}
      </Card>
    </div>
  );
}
