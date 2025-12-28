from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud, schemas
from core.database import get_db_session

app = FastAPI(title="URL Shortener")

#Эндпоинт для созжания коротого URL
@app.post(path="/shorten", response_model=schemas.URLInfo)
async def create_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db_session)):
    return await crud.create_bd_urls(db=db, url=url)


#Эндпоинт для редиректа
@app.get(path="/{url_key}")
async def forward_to_target_url(url_key: str, db: AsyncSession = Depends(get_db_session)):
    db_url = await crud.get_db_url_by_key(db=db, url_key=url_key)

    if db_url:
        await crud.update_db_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.original_url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
    


#"Cтатистика"
@app.get(path="/stats/{url_key}")
async def get_url_status(url_key: str, db: AsyncSession = Depends(get_db_session)):
    db_url = await crud.get_db_url_by_key(db=db, url_key=url_key)

    if db_url:
        return db_url
    raise HTTPException(status_code=404, detail="URL not found")