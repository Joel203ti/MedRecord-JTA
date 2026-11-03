from pydantic import BaseModel, Field
class Question(BaseModel):
    question: str = Field(min_length=3,max_length=500)
    document_text: str = Field(min_length=1,max_length=120000)
class ReportRequest(BaseModel):
    summary: dict
    filename: str = "expediente.pdf"
