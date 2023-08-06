from tva_utils.postgres.schemas import BaseModel

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.session import Session
from sqlalchemy import text, inspect
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import DeclarativeMeta
import sqlalchemy
import logging

from typing import List, Union, Iterator
import uuid


class DB:
    def initialize(cls, url: str, logger: logging.Logger = None, **kwargs):
        cls.engine: Engine = get_engine(url, **kwargs)
        cls.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.engine
        )
        cls.inspector = inspect(cls.engine)
        cls.logger = logger

        if cls.logger is None:
            cls.logger = logging.getLogger("uvicorn.error")

        cls.utils = DBUtils(cls.logger)

        cls.logger.info("Initialized DB")

    def create_tables(
        cls, Bases: List[DeclarativeMeta], schemas: List[str] = ["public"]
    ):
        """
        Creates tables for all the models in the list of Bases
        """
        if type(Bases) != list:
            Bases = [Bases]

        if type(schemas) != list:
            schemas = [schemas]

        for Base, schema in zip(Bases, schemas):
            try:
                if schema not in cls.inspector.get_schema_names():
                    cls.engine.execute(sqlalchemy.schema.CreateSchema(schema))
                Base.metadata.create_all(cls.engine)
            except Exception as e:
                cls.logger.info(f"Error in create_tables: {e}")

    def get_session(cls) -> Iterator[Session]:
        with cls.SessionLocal() as session:
            try:
                yield session
            finally:
                session.close()

    def get_session_scoped(cls) -> scoped_session:
        return scoped_session(cls.SessionLocal)

    def close(cls):
        cls.engine.dispose()


class DBUtils:
    def __init__(cls, logger: logging.Logger):
        cls.session = None
        cls.logger = logger

    def initialize(cls, session: Session):
        cls.session = session

    @staticmethod
    def wrap_to_json(stmt: str) -> text:
        stmt = stmt.replace(";", "")
        return text(f"SELECT json_agg(t) FROM ({stmt}) t")

    def select(cls, session: Session, sql: str) -> Union[List[dict], None]:
        try:
            stmt: text = cls.wrap_to_json(sql)
            results = session.execute(stmt).fetchone()[0]
            if results is None:
                return []

            return results
        except DBAPIError as e:
            raise e

    def execute(cls, session: Session, sql: str) -> Union[bool, None]:
        try:
            stmt: text = text(sql)
            session.execute(stmt)

            return True
        except DBAPIError as e:
            raise e

    def select_with_params(
        cls,
        session: Session,
        sql: str,
        params: dict,
    ) -> Union[List[dict], None]:
        try:
            stmt: text = cls.wrap_to_json(sql)
            results = session.execute(stmt, params=params).fetchone()[0]

            if results is None:
                return []

            return results
        except DBAPIError as e:
            cls.logger.info(f"Error in select_stmt_raw_sql_params: {e}")
            raise e

    def add_record(cls, session: Session, model, kwargs) -> Union[object, None]:
        try:
            obj = model(**kwargs)
            session.add(obj)
            session.commit()
            return obj
        except DBAPIError as e:
            cls.logger.info(f"Error in add_record_sync: {e}")
            session.rollback()
            return None

    def add_records(
        cls, session: Session, model: BaseModel, records: List[dict]
    ) -> Union[List[uuid.UUID], List[BaseModel]]:
        try:
            inserted_ids = []

            records_to_insert: List[BaseModel] = [model(**record) for record in records]

            session.add_all(records_to_insert)
            session.flush()  # Flush the records to obtain their IDs

            records: dict = [record.to_dict() for record in records_to_insert]
            for record in records_to_insert:
                inserted_ids.append(record.uuid)
            session.commit()
            return inserted_ids, records
        except DBAPIError as e:
            cls.session.rollback()
            cls.logger.info(f"Error in add_records_sync: {e}")
            return [], []

    def add_records_on_conflict(
        cls,
        session: Session,
        model: BaseModel,
        records: List[dict],
    ):
        for record in records:
            cls.add_record(session, model, record)

    def remove_records(
        cls, session: Session, model: BaseModel, records: List[uuid.UUID]
    ) -> bool:
        try:
            session.query(model).filter(model.uuid.in_(records)).delete(
                synchronize_session=False
            )
            session.commit()
            cls.logger.info(f"Deleted {len(records)} records")
            return True
        except DBAPIError as e:
            session.rollback()
            cls.logger.info(f"Error in remove_records_sync: {e}")
            return False


def get_engine(url: str, **kwargs) -> Engine:
    try:
        return create_engine(
            url,
            **kwargs,
            # pool_size=5,
            # max_overflow=0,
            # pool_pre_ping=True,
        )
    except DBAPIError as e:
        raise e


db = DB()
