from typing import Any

from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {
            dict[str, Any]: JSON
        }