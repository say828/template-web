from contexts.shipping.domain import (
    ShippingCarrierLoad,
    ShippingOverview,
    ShippingStat,
    ShipmentStatusTransition,
    ShipmentSummary,
    UpdateShipmentStatusCommand,
)
from contexts.shipping.infrastructure import (
    list_seed_shipments,
    transition_seed_shipment_status,
)


def get_shipping_overview() -> ShippingOverview:
    records = list_seed_shipments()
    in_transit_count = sum(
        1
        for record in records
        if record.status in {"In transit", "Out for delivery", "Delayed"}
    )
    delayed_count = sum(1 for record in records if record.status == "Delayed")
    delivered_today_count = sum(1 for record in records if record.delivered_today)

    carrier_names = sorted({record.carrier for record in records})
    carriers = []
    for carrier in carrier_names:
        carrier_records = [record for record in records if record.carrier == carrier]
        delayed_for_carrier = sum(
            1 for record in carrier_records if record.status == "Delayed"
        )
        carriers.append(
            ShippingCarrierLoad(
                label=carrier,
                value=f"{len(carrier_records)}건 · 지연 {delayed_for_carrier}건",
            )
        )

    highlighted = next(
        (record for record in records if record.status == "Delayed"),
        records[0],
    )

    return ShippingOverview(
        stats=[
            ShippingStat(
                label="배송 중",
                value=str(in_transit_count),
                tone="text-[var(--in-accent)]",
            ),
            ShippingStat(
                label="지연",
                value=str(delayed_count),
                tone="text-[#c4663a]",
            ),
            ShippingStat(
                label="오늘 완료",
                value=str(delivered_today_count),
                tone="text-[#245f92]",
            ),
        ],
        carriers=carriers,
        highlighted_route=(
            f"{highlighted.route_name} · {highlighted.last_event}"
        ),
    )


def get_shipment_list() -> list[ShipmentSummary]:
    return [
        ShipmentSummary(
            shipment_id=record.shipment_id,
            order_id=record.order_id,
            carrier=record.carrier,
            destination=record.destination,
            tracking_number=record.tracking_number,
            status=record.status,
            eta=record.eta,
            last_event=record.last_event,
        )
        for record in list_seed_shipments()
    ]


def transition_shipment_status(
    shipment_id: str, command: UpdateShipmentStatusCommand
) -> ShipmentStatusTransition:
    return transition_seed_shipment_status(shipment_id, command)


def prepare_shipping_store() -> None:
    list_seed_shipments()
