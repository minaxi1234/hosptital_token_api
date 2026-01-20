from fastapi import APIRouter
from pydantic import BaseModel

from app.assistant.service import AssistantService
import app.assistant.state as assistant_state


router = APIRouter(prefix="/assistant", tags=["Assistant"])



class AssistantRequest(BaseModel):
    question: str


class AssistantResponse(BaseModel):
    question: str
    answer: str


@router.post("/ask", response_model=AssistantResponse)
def ask_assistant(request: AssistantRequest):
    if assistant_state.assistant_service is None:
        return{
            "question": request.question,
            "answer": "Assistant is initializing. Please try again"
        }
    return assistant_state.assistant_service.ask(request.question)
