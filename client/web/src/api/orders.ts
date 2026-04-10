import { apiGet } from "@/api/client";

export interface DashboardStat {
  label: string;
  value: string;
  tone?: string | null;
}

export interface OrderActivity {
  order_id: string;
  date: string;
  customer: string;
  status: string;
}

export interface SelectedOrder {
  product_name: string;
  customer_name: string;
  status: string;
  amount: string;
}

export interface OrderOverviewResponse {
  stats: DashboardStat[];
  recent_activity: OrderActivity[];
  selected_order: SelectedOrder;
}

export interface OrderSummary {
  id: string;
  product_name: string;
  customer_name: string;
  status: string;
}

export function fetchOrderOverview(accessToken: string) {
  return apiGet<OrderOverviewResponse>("/orders/overview", { accessToken });
}

export function fetchOrders(accessToken: string) {
  return apiGet<OrderSummary[]>("/orders", { accessToken });
}
