from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.exception_handling import ExceptionHandling

# Database connection string
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:localhost@localhost/ai_fastapi"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 # Base class for SQLAlchemy models
Base = declarative_base()


def create_db_query(tb_name, filters):
    db_query = ''
    try:
        db_query = f"db.query({tb_name})"

        list_filter = {key: value for key, value in filters.items() if isinstance(value, list)}
        in_filters = ''
        for k, v in list_filter.items():
            in_filters += f'{tb_name}.{k}.in_({v})'
            filters.pop(k)

        db_query += f".filter({in_filters})"
        if filters:
            db_query += f".filter_by(**{filters})"

    except Exception as e:
        ExceptionHandling(e=str(e), function_name='create_db_query').exception_handling(
            message=False)
        db_query = ''

    return db_query
