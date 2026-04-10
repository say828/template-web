import { useEffect, useState } from "react";
import { Search } from "lucide-react";

import { useAuth } from "@/auth/AuthProvider";
import { fetchOrders, type OrderSummary } from "@/api/orders";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export function OrdersPage() {
  const { token } = useAuth();
  const [orders, setOrders] = useState<OrderSummary[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token?.access_token) {
      return;
    }

    let cancelled = false;

    setLoading(true);
    setError(null);

    fetchOrders(token.access_token)
      .then((response) => {
        if (!cancelled) {
          setOrders(response);
        }
      })
      .catch((nextError: Error) => {
        if (!cancelled) {
          setError(nextError.message);
          setOrders([]);
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

  const normalizedQuery = query.trim().toLowerCase();
  const filteredOrders = orders.filter((order) =>
    [order.id, order.product_name, order.customer_name, order.status].some((field) =>
      field.toLowerCase().includes(normalizedQuery),
    ),
  );

  return (
    <div className="space-y-6">
      <Card className="p-[var(--app-card-padding)]">
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative min-w-[280px] flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#8d97a8]" />
            <Input className="pl-9" placeholder="Search orders" value={query} onChange={(event) => setQuery(event.target.value)} />
          </div>
          <Button variant="outline" onClick={() => setQuery("")}>
            Reset
          </Button>
          <Button>New order</Button>
        </div>
        <p className="mt-4 text-sm text-[var(--app-muted)]">
          {loading ? "Loading order list..." : `Showing ${filteredOrders.length} of ${orders.length} orders`}
        </p>
      </Card>

      <Card className="overflow-hidden">
        <table className="w-full border-collapse text-sm">
          <thead className="bg-[#f8fafe] text-left text-[#516174]">
            <tr>
              {["Order", "Product", "Customer", "Status"].map((cell) => (
                <th key={cell} className="border-y border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] font-semibold">
                  {cell}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-muted)]" colSpan={4}>
                  Loading orders...
                </td>
              </tr>
            ) : null}
            {error ? (
              <tr>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-danger)]" colSpan={4}>
                  {error}
                </td>
              </tr>
            ) : null}
            {!loading && !error && !filteredOrders.length ? (
              <tr>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-muted)]" colSpan={4}>
                  No orders matched the current search.
                </td>
              </tr>
            ) : null}
            {filteredOrders.map((order) => (
              <tr key={order.id}>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)] text-[var(--app-accent)]">{order.id}</td>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">{order.product_name}</td>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">{order.customer_name}</td>
                <td className="border-b border-[var(--app-border)] px-[var(--app-table-cell-px)] py-[var(--app-table-cell-py)]">
                  <span className={order.status === "At risk" ? "text-[var(--app-danger)]" : "text-[#314157]"}>{order.status}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
