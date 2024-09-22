from fastapi import APIRouter, FastAPI
from application.interfaces.expression_request_payload import ExpressionCalculateRequest

app = FastAPI()
router = APIRouter()

@router.post("/expression/calculate/")
def create_item(request: ExpressionCalculateRequest):
    return request

app.include_router(router)