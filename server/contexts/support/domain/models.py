from pydantic import BaseModel


class SupportFaq(BaseModel):
    id: str
    question: str
    visibility: str


class SupportFaqRecord(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    visibility: str
    updated_at: str


class CreateSupportFaqCommand(BaseModel):
    question: str
    answer: str
    category: str = "General"
    visibility: str = "노출"


class ChangeFaqVisibilityCommand(BaseModel):
    visibility: str
