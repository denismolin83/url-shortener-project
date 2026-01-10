from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

import crud, schemas
from core.database import get_db_session

app = FastAPI(
    title="URL Shortener",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs")

#Настрока CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")


@app.exception_handler(RequestValidationError)
async def valedation_exception_handler(request: Request, exc: RequestValidationError):

    errors = exc.errors()

    custom_msg = "Некорректный адрес: "
    if errors:
        err = errors[0]
        if err['type'] == 'url_parsing':
            custom_msg += "убедитесь, что указан протокол (http:// или https://)"
        elif err['type'] == 'url_scheme':
            custom_msg += "поддерживаются только протоколы http и https"
        else:
            custom_msg += err.get('msg', 'неизвестная ошибка валидации')

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": custom_msg}
    )



#Эндпоинт для созжания коротого URL
@router.post(path="/shorten", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.create_bd_urls(db=db, url=url)


#Эндпоинт для редиректа
@router.get(path="/{url_key}")
async def forward_to_target_url(url_key: str, db: AsyncSession = Depends(get_db_session)):
    db_url = await crud.get_db_url_by_key(db=db, url_key=url_key)

    if db_url:
        await crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
    


#"Cтатистика"
@router.get(path="/stats/{url_key}")
async def get_url_status(url_key: str, db: AsyncSession = Depends(get_db_session)):
    db_url = await crud.get_db_url_by_key(db=db, url_key=url_key)

    if db_url:
        return db_url
    raise HTTPException(status_code=404, detail="URL not found")


app.include_router(router=router)