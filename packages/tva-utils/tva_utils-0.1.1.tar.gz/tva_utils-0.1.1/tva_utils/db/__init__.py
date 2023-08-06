"""Main entrypoint into package."""
from tva_utils.db.postgres import DB
from tva_utils.db.schemas import BaseModel

__all__ = ["DB"]