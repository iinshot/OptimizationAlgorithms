from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from optimization_service import OptimizationService

router = APIRouter()

class OptimizeRequest(BaseModel):
    algorithm: str
    function: str
    params: Dict[str, Any]

@router.post("/optimize")
def optimize(req: OptimizeRequest):
    service = OptimizationService()
    result = service.run(
        req.algorithm,
        req.function,
        req.params
    )
    return result