from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..packages.helpers import decode_token

router = APIRouter(tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = await decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401, detail="Неверный токен или срок действия истёк"
        )

    return {"msg": f"Добро пожаловать, {payload['sub']}!"}
