from sqlalchemy import String
from core.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    short_key: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    original_url: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    hits: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<URL(id={self.id}, short_key={self.short_key}, original_url={self.original_url})"