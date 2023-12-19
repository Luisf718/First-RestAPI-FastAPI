from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, HTTPException
##Importamos la función que genera el token para autenticación del usuario
from utils.jwt_manager import validate_token


###Clase para pedir autenticación en determinadas rutas
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request): #-> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials")