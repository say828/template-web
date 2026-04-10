from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.http.app import app
from contexts.auth.application import services as auth_services
from contexts.auth.infrastructure import repository as auth_repository
from contexts.alerts.infrastructure import repository as alerts_repository
from contexts.catalog.application import services as catalog_services
from contexts.catalog.infrastructure import repository as catalog_repository
from contexts.fulfillment.infrastructure import repository as fulfillment_repository
from contexts.inventory.application import services as inventory_services
from contexts.inventory.infrastructure import repository as inventory_repository
from contexts.orders.infrastructure import repository as orders_repository
from contexts.shipping.infrastructure import repository as shipping_repository
from contexts.support.infrastructure import repository as support_repository
from contexts.user.infrastructure import factory as user_factory


ADMIN_EMAIL = "admin@example.com"
OPERATOR_EMAIL = "operator@example.com"
PASSWORD = "<CHANGE_ME>"


@pytest.fixture(autouse=True)
def reset_in_memory_state() -> Generator[None, None, None]:
    auth_services._seed_auth_store.cache_clear()
    auth_repository.get_auth_repository.cache_clear()
    catalog_services._seed_catalog_store.cache_clear()
    catalog_repository.get_catalog_repository.cache_clear()
    inventory_services._seed_inventory_store.cache_clear()
    inventory_repository.get_inventory_repository.cache_clear()
    user_factory.get_user_repository.cache_clear()
    alerts_repository._alert_store = None
    orders_repository._order_store = None
    shipping_repository._shipment_store = None
    support_repository._support_faq_store = None
    fulfillment_repository._task_store = None
    fulfillment_repository._event_store = None
    fulfillment_repository._note_store = None
    yield
    auth_services._seed_auth_store.cache_clear()
    auth_repository.get_auth_repository.cache_clear()
    catalog_services._seed_catalog_store.cache_clear()
    catalog_repository.get_catalog_repository.cache_clear()
    inventory_services._seed_inventory_store.cache_clear()
    inventory_repository.get_inventory_repository.cache_clear()
    user_factory.get_user_repository.cache_clear()
    alerts_repository._alert_store = None
    orders_repository._order_store = None
    shipping_repository._shipment_store = None
    support_repository._support_faq_store = None
    fulfillment_repository._task_store = None
    fulfillment_repository._event_store = None
    fulfillment_repository._note_store = None


def _login(client: TestClient, email: str = ADMIN_EMAIL) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": PASSWORD},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_aut_f001_login_and_me_issue_authenticated_identity() -> None:
    with TestClient(app) as client:
        token = _login(client)
        me_response = client.get("/api/v1/auth/me", headers=_auth_headers(token))

    assert me_response.status_code == 200
    assert me_response.json() == {
        "id": "user-1",
        "name": "Template Admin",
        "email": ADMIN_EMAIL,
        "role": "admin",
        "status": "active",
    }


def test_usr_f001_admin_can_read_and_update_users_while_operator_is_forbidden() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        operator_token = _login(client, OPERATOR_EMAIL)

        forbidden_response = client.get("/api/v1/users", headers=_auth_headers(operator_token))
        list_response = client.get("/api/v1/users", headers=_auth_headers(admin_token))
        detail_response = client.get("/api/v1/users/user-2", headers=_auth_headers(admin_token))
        patch_response = client.patch(
            "/api/v1/users/user-2/status",
            json={"status": "suspended"},
            headers=_auth_headers(admin_token),
        )

    assert forbidden_response.status_code == 403
    assert list_response.status_code == 200
    assert len(list_response.json()) == 2
    assert detail_response.status_code == 200
    assert detail_response.json()["email"] == OPERATOR_EMAIL
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "suspended"


def test_cat_f001_public_catalog_read_surfaces_return_live_product_data() -> None:
    with TestClient(app) as client:
        list_response = client.get("/api/v1/catalog/products")
        filtered_response = client.get("/api/v1/catalog/products", params={"status": "active"})
        detail_response = client.get("/api/v1/catalog/products/prd-1001")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 3
    assert filtered_response.status_code == 200
    assert len(filtered_response.json()) == 1
    assert detail_response.status_code == 200
    assert detail_response.json()["slug"] == "trailshell-pack-jacket"


def test_cat_f002_admin_can_create_update_and_archive_catalog_products() -> None:
    payload = {
        "slug": "metro-pack-vest",
        "name": "Metro Pack Vest",
        "brand": "Northstar Supply",
        "category": "outerwear",
        "status": "draft",
        "short_description": "Packable insulated vest for shoulder-season layering.",
        "description": "Metro Pack Vest blends light insulation with a compact stow pouch for travel days.",
        "hero_image": {
            "url": "https://images.templates.dev/catalog/metro-pack-vest/hero.jpg",
            "alt": "Metro Pack Vest in slate",
        },
        "gallery": [],
        "price": {"amount": 149000, "currency": "KRW"},
        "compare_at_price": None,
        "tags": ["new-drop"],
        "attributes": [{"name": "Fit", "value": "Regular"}],
        "variants": [
            {
                "sku": "MPV-SLT-M",
                "name": "Slate / M",
                "option_values": ["Slate", "M"],
            }
        ],
    }

    with TestClient(app) as client:
        admin_token = _login(client)
        create_response = client.post(
            "/api/v1/catalog/products",
            json=payload,
            headers=_auth_headers(admin_token),
        )
        created_product_id = create_response.json()["id"]
        update_response = client.put(
            f"/api/v1/catalog/products/{created_product_id}",
            json={
                "short_description": "Packable insulated vest for transit and weekend travel.",
                "tags": ["new-drop", "travel"],
            },
            headers=_auth_headers(admin_token),
        )
        status_response = client.patch(
            f"/api/v1/catalog/products/{created_product_id}/status",
            json={"status": "archived"},
            headers=_auth_headers(admin_token),
        )

    assert create_response.status_code == 201
    assert create_response.json()["slug"] == payload["slug"]
    assert update_response.status_code == 200
    assert update_response.json()["short_description"].startswith("Packable insulated vest")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "archived"


def test_inv_f001_admin_can_read_and_mutate_inventory_levels() -> None:
    with TestClient(app) as client:
        admin_token = _login(client)
        operator_token = _login(client, OPERATOR_EMAIL)

        forbidden_response = client.get("/api/v1/inventory/levels", headers=_auth_headers(operator_token))
        list_response = client.get("/api/v1/inventory/levels", headers=_auth_headers(admin_token))
        detail_response = client.get(
            "/api/v1/inventory/levels/TSJ-BLK-S/fc-seoul",
            headers=_auth_headers(admin_token),
        )
        adjust_response = client.post(
            "/api/v1/inventory/levels/TSJ-BLK-S/fc-seoul/adjustments",
            json={"quantity_delta": 4, "reason": "cycle_count"},
            headers=_auth_headers(admin_token),
        )
        reserve_response = client.post(
            "/api/v1/inventory/levels/TSJ-BLK-S/fc-seoul/reservations",
            json={"quantity": 2, "reference_id": "ORD-NEW-1"},
            headers=_auth_headers(admin_token),
        )
        release_response = client.post(
            "/api/v1/inventory/levels/TSJ-BLK-S/fc-seoul/releases",
            json={"quantity": 1, "reference_id": "ORD-NEW-1"},
            headers=_auth_headers(admin_token),
        )
        set_response = client.put(
            "/api/v1/inventory/levels/TSJ-BLK-S/fc-seoul",
            json={
                "on_hand": 20,
                "reserved": 3,
                "safety_stock": 4,
                "reorder_point": 8,
            },
            headers=_auth_headers(admin_token),
        )

    assert forbidden_response.status_code == 403
    assert list_response.status_code == 200
    assert len(list_response.json()) == 6
    assert detail_response.status_code == 200
    assert detail_response.json()["available_to_sell"] == 15
    assert adjust_response.status_code == 200
    assert adjust_response.json()["action"] == "adjusted"
    assert adjust_response.json()["level"]["on_hand"] == 22
    assert reserve_response.status_code == 200
    assert reserve_response.json()["level"]["reserved"] == 5
    assert release_response.status_code == 200
    assert release_response.json()["level"]["reserved"] == 4
    assert set_response.status_code == 200
    assert set_response.json()["level"]["available_to_sell"] == 17


def test_ord_f001_authenticated_users_can_read_create_and_update_orders() -> None:
    with TestClient(app) as client:
        operator_token = _login(client, OPERATOR_EMAIL)

        unauthorized_response = client.get("/api/v1/orders")
        overview_response = client.get("/api/v1/orders/overview", headers=_auth_headers(operator_token))
        list_response = client.get("/api/v1/orders", headers=_auth_headers(operator_token))
        create_response = client.post(
            "/api/v1/orders",
            json={
                "product_id": "prd-1002",
                "product_name": "Commuter Utility Sling",
                "customer_name": "Daegu Concept Store",
                "seller_name": "Harbor Line",
                "amount_krw": 129000,
                "stage": "결제 검증",
                "status": "Pending",
                "fulfillment_status": "Queued",
                "sla": "35 min",
            },
            headers=_auth_headers(operator_token),
        )
        created_order_id = create_response.json()["id"]
        status_response = client.patch(
            f"/api/v1/orders/{created_order_id}/status",
            json={
                "status": "Paid",
                "fulfillment_status": "Packing",
                "stage": "패킹 준비",
            },
            headers=_auth_headers(operator_token),
        )

    assert unauthorized_response.status_code == 401
    assert overview_response.status_code == 200
    assert overview_response.json()["selected_order"]["product_name"]
    assert list_response.status_code == 200
    assert len(list_response.json()) == 4
    assert create_response.status_code == 201
    assert create_response.json()["customer_name"] == "Daegu Concept Store"
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "Paid"
    assert status_response.json()["fulfillment_status"] == "Packing"


def test_ord_f002_admin_only_order_surfaces_require_admin_role() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        operator_token = _login(client, OPERATOR_EMAIL)

        forbidden_response = client.get(
            "/api/v1/orders/admin/overview",
            headers=_auth_headers(operator_token),
        )
        overview_response = client.get(
            "/api/v1/orders/admin/overview",
            headers=_auth_headers(admin_token),
        )
        queue_response = client.get(
            "/api/v1/orders/admin/queue",
            headers=_auth_headers(admin_token),
        )

    assert forbidden_response.status_code == 403
    assert overview_response.status_code == 200
    assert len(overview_response.json()["cards"]) == 3
    assert "alerts" not in overview_response.json()
    assert queue_response.status_code == 200
    assert queue_response.json()[0]["product_name"]


def test_sup_f001_admin_can_read_create_and_hide_support_faqs() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        operator_token = _login(client, OPERATOR_EMAIL)

        forbidden_response = client.get(
            "/api/v1/support/faqs",
            headers=_auth_headers(operator_token),
        )
        list_response = client.get(
            "/api/v1/support/faqs",
            headers=_auth_headers(admin_token),
        )
        create_response = client.post(
            "/api/v1/support/faqs",
            json={
                "question": "교환 요청은 어디서 확인하나요?",
                "answer": "교환 요청은 운영 지원 큐와 주문 상세에서 함께 확인합니다.",
                "category": "교환",
                "visibility": "노출",
            },
            headers=_auth_headers(admin_token),
        )
        created_faq_id = create_response.json()["id"]
        visibility_response = client.patch(
            f"/api/v1/support/faqs/{created_faq_id}/visibility",
            json={"visibility": "숨김"},
            headers=_auth_headers(admin_token),
        )

    assert forbidden_response.status_code == 403
    assert list_response.status_code == 200
    assert len(list_response.json()) == 3
    assert create_response.status_code == 201
    assert create_response.json()["category"] == "교환"
    assert visibility_response.status_code == 200
    assert visibility_response.json()["visibility"] == "숨김"


def test_ful_f001_authenticated_users_can_read_and_transition_fulfillment_tasks() -> None:
    with TestClient(app) as client:
        operator_token = _login(client, OPERATOR_EMAIL)

        unauthorized_response = client.get("/api/v1/fulfillment/overview")
        overview_response = client.get(
            "/api/v1/fulfillment/overview",
            headers=_auth_headers(operator_token),
        )
        board_response = client.get(
            "/api/v1/fulfillment/board",
            headers=_auth_headers(operator_token),
        )
        transition_response = client.patch(
            "/api/v1/fulfillment/tasks/ft-1/status",
            json={"status": "In progress", "stage": "Packing"},
            headers=_auth_headers(operator_token),
        )

    assert unauthorized_response.status_code == 401
    assert overview_response.status_code == 200
    assert overview_response.json()["throughput_total"] == "5"
    assert board_response.status_code == 200
    assert len(board_response.json()["tasks"]) == 4
    assert len(board_response.json()["notes"]) == 3
    assert transition_response.status_code == 200
    assert transition_response.json()["previous_status"] == "Queued"
    assert transition_response.json()["status"] == "In progress"


def test_shp_f001_authenticated_users_can_read_shipping_overview() -> None:
    with TestClient(app) as client:
        operator_token = _login(client, OPERATOR_EMAIL)

        unauthorized_response = client.get("/api/v1/shipping/overview")
        overview_response = client.get(
            "/api/v1/shipping/overview",
            headers=_auth_headers(operator_token),
        )

    assert unauthorized_response.status_code == 401
    assert overview_response.status_code == 200
    assert len(overview_response.json()["stats"]) == 3
    assert len(overview_response.json()["carriers"]) == 3
    assert overview_response.json()["highlighted_route"]


def test_shp_f002_authenticated_users_can_read_shipping_shipments() -> None:
    with TestClient(app) as client:
        operator_token = _login(client, OPERATOR_EMAIL)
        list_response = client.get(
            "/api/v1/shipping/shipments",
            headers=_auth_headers(operator_token),
        )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 4
    assert list_response.json()[0]["shipment_id"] == "shp-1001"
    assert list_response.json()[0]["tracking_number"]


def test_shp_f003_authenticated_users_can_transition_shipping_shipments() -> None:
    with TestClient(app) as client:
        operator_token = _login(client, OPERATOR_EMAIL)
        transition_response = client.patch(
            "/api/v1/shipping/shipments/shp-1001/status",
            json={"status": "Delivered", "last_event": "고객 인수 완료"},
            headers=_auth_headers(operator_token),
        )
        list_response = client.get(
            "/api/v1/shipping/shipments",
            headers=_auth_headers(operator_token),
        )

    assert transition_response.status_code == 200
    assert transition_response.json()["shipment_id"] == "shp-1001"
    assert transition_response.json()["previous_status"] == "In transit"
    assert transition_response.json()["status"] == "Delivered"
    assert transition_response.json()["last_event"] == "고객 인수 완료"
    assert list_response.status_code == 200
    assert list_response.json()[0]["status"] == "Delivered"


def test_alr_f001_admin_only_alert_feed_requires_admin_role() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        operator_token = _login(client, OPERATOR_EMAIL)

        forbidden_response = client.get(
            "/api/v1/alerts",
            headers=_auth_headers(operator_token),
        )
        list_response = client.get(
            "/api/v1/alerts",
            headers=_auth_headers(admin_token),
        )

    assert forbidden_response.status_code == 403
    assert list_response.status_code == 200
    assert list_response.json()["unread_count"] == 3
    assert len(list_response.json()["items"]) == 4


def test_alr_f002_admin_can_mark_single_alert_as_read() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        read_response = client.post(
            "/api/v1/alerts/alr-1001/read",
            headers=_auth_headers(admin_token),
        )
        list_response = client.get(
            "/api/v1/alerts",
            headers=_auth_headers(admin_token),
        )

    assert read_response.status_code == 200
    assert read_response.json()["id"] == "alr-1001"
    assert read_response.json()["read"] is True

    assert list_response.status_code == 200
    assert list_response.json()["unread_count"] == 2


def test_alr_f003_admin_can_mark_all_alerts_as_read() -> None:
    with TestClient(app) as client:
        admin_token = _login(client, ADMIN_EMAIL)
        read_all_response = client.post(
            "/api/v1/alerts/read-all",
            headers=_auth_headers(admin_token),
        )
        list_response = client.get(
            "/api/v1/alerts",
            headers=_auth_headers(admin_token),
        )

    assert read_all_response.status_code == 200
    assert read_all_response.json()["updated_count"] == 3
    assert read_all_response.json()["unread_count"] == 0
    assert list_response.status_code == 200
    assert list_response.json()["unread_count"] == 0
