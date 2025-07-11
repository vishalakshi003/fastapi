# shared/core/context.py
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class CustomContext:
    def __init__(
        self,
        request: Request,
        db: AsyncSession,
        user: Optional[str] = None,
    ):
        self.request = request
        self.db = db
        self.user = user