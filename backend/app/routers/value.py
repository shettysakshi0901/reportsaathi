
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from ..models.database import SessionLocal
from ..models.value import ValueModel

router = APIRouter()

@router.get("/value")
async def get_value():
    with SessionLocal() as db:
        result = db.execute(select(ValueModel)).first()

        if result:
            value = result[0].value
        else:
            value = "No data"

    return JSONResponse({"value": value})
