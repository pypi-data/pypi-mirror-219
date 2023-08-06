"""Main entrypoint into package."""
from tva_utils.postgres.postgres import DB, db
from tva_utils.postgres.schemas import BaseModel

__all__ = ["DB", "db", "BaseModel"]