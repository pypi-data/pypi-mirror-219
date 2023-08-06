from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
from sqlalchemy import inspect
import uuid


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


    created_at = Column(TIMESTAMP, nullable=False, server_default=text("NOW()"))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def table_name(self):
        return f"{self.__table_args__['schema']}.{self.__tablename__}"

