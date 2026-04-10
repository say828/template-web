from contexts.support.domain import (
    ChangeFaqVisibilityCommand,
    CreateSupportFaqCommand,
    SupportFaq,
    SupportFaqRecord,
)
from contexts.support.infrastructure import (
    create_seed_support_faq,
    list_seed_support_faqs,
    update_seed_support_faq_visibility,
)


def get_support_faqs() -> list[SupportFaq]:
    return list_seed_support_faqs()


def create_support_faq(command: CreateSupportFaqCommand) -> SupportFaqRecord:
    return create_seed_support_faq(command)


def change_faq_visibility(
    faq_id: str, command: ChangeFaqVisibilityCommand
) -> SupportFaqRecord:
    return update_seed_support_faq_visibility(faq_id, command)


def prepare_support_store() -> None:
    list_seed_support_faqs()
