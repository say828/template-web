from fastapi import APIRouter, Depends, HTTPException

from contexts.auth.contracts.http.dependencies import require_admin_user
from contexts.support.application import (
    change_faq_visibility,
    create_support_faq,
    get_support_faqs,
)
from contexts.support.domain import (
    ChangeFaqVisibilityCommand,
    CreateSupportFaqCommand,
    SupportFaq,
    SupportFaqRecord,
)

router = APIRouter(
    prefix="/support",
    tags=["support"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("/faqs", response_model=list[SupportFaq])
def support_faqs() -> list[SupportFaq]:
    return get_support_faqs()


@router.post("/faqs", response_model=SupportFaqRecord, status_code=201)
def create_support_faq_entry(command: CreateSupportFaqCommand) -> SupportFaqRecord:
    return create_support_faq(command)


@router.patch("/faqs/{faq_id}/visibility", response_model=SupportFaqRecord)
def change_support_faq_visibility(
    faq_id: str, command: ChangeFaqVisibilityCommand
) -> SupportFaqRecord:
    try:
        return change_faq_visibility(faq_id, command)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
