from datetime import date

from contexts.support.domain import (
    ChangeFaqVisibilityCommand,
    CreateSupportFaqCommand,
    SupportFaq,
    SupportFaqRecord,
)
from data.bootstrap_loader import load_bootstrap_json

_support_faq_store: list[SupportFaqRecord] | None = None


def _get_support_faq_store() -> list[SupportFaqRecord]:
    global _support_faq_store
    if _support_faq_store is None:
        _support_faq_store = [
            SupportFaqRecord(**entry)
            for entry in load_bootstrap_json("support_faqs.json")
        ]
    return _support_faq_store


def _copy_support_faq(record: SupportFaqRecord) -> SupportFaqRecord:
    return record.model_copy(deep=True)


def _next_faq_number(records: list[SupportFaqRecord]) -> int:
    return max((int(record.id.split("-")[-1]) for record in records), default=0) + 1


def list_seed_support_faqs() -> list[SupportFaq]:
    return [
        SupportFaq(id=record.id, question=record.question, visibility=record.visibility)
        for record in _get_support_faq_store()
    ]


def create_seed_support_faq(command: CreateSupportFaqCommand) -> SupportFaqRecord:
    records = _get_support_faq_store()
    record = SupportFaqRecord(
        id=f"faq-{_next_faq_number(records)}",
        question=command.question,
        answer=command.answer,
        category=command.category,
        visibility=command.visibility,
        updated_at=date.today().isoformat(),
    )
    records.insert(0, record)
    return _copy_support_faq(record)


def update_seed_support_faq_visibility(
    faq_id: str, command: ChangeFaqVisibilityCommand
) -> SupportFaqRecord:
    records = _get_support_faq_store()
    for index, record in enumerate(records):
        if record.id != faq_id:
            continue

        updated_record = record.model_copy(
            update={
                "visibility": command.visibility,
                "updated_at": date.today().isoformat(),
            }
        )
        records[index] = updated_record
        return _copy_support_faq(updated_record)

    raise LookupError(f"Support FAQ {faq_id} not found")
