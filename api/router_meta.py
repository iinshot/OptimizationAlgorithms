from fastapi import APIRouter
from domain.factory import Factory

router = APIRouter()

@router.get("/meta")
def meta():
    algorithms = []
    for algo in Factory.algorithms.values():
        algorithms.append({
            "name": algo.name,
            "label": algo.label,
            "parameters": [p.model_dump() for p in algo.parameters]
        })

    functions = []
    for func in Factory.functions.values():
        functions.append({
            "name": func.name,
            "label": func.label,
            "parameters": getattr(func, "parameters", [])
        })

    return {
        "algorithms": algorithms,
        "functions": functions
    }