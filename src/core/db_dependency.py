from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session


db_session = Annotated[AsyncSession, Depends(get_db_session)]