from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas
import utils


async def create_bd_urls(db: AsyncSession, url: schemas.URLCreate) -> models.URL:

    #Проверяем есть ли в базе такой же url, если есть возвращем его
    result = await db.execute(
        select(models.URL).where(models.URL.original_url == str(url.target_url))
    )
    existing_url = result.scalars().first()
    if existing_url:
        return existing_url
    
    #Проверка есть ли в базе уже такой ключ, генерируем пока не получим еще не имеющийся
    while True:
        key = utils.create_random_key()

        key_check = await db.execute(
            select(models.URL).where(models.URL.short_key == key)
        )
        if not key_check.scalars().first():
            break
    

    db_url = models.URL(
        original_url=str(url.target_url),
        short_key=key
    )

    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url



async def get_db_url_by_key(db: AsyncSession, url_key: str) -> models.URL:
    result = await db.execute(select(models.URL).where(models.URL.short_key == url_key))
    return result.scalars().first()


async def update_db_clicks(db: AsyncSession, db_url: models.URL):
    db_url.hits+=1
    await db.commit()
    await db.refresh(db_url)
    return db_url