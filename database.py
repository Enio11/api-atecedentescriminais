from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import List, Optional, Any
import json

DATABASE_URL = "sqlite:///./requests.db"

Base = declarative_base()


class RequestLog(Base):  # type: ignore
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    document = Column(String, index=True)
    status = Column(String)
    records_count = Column(Integer, default=0)
    details = Column(Text, default="[]")  # JSON string of process numbers
    names = Column(Text, default="[]")  # JSON string of party names


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)  # type: ignore


def log_request(
    document: str,
    status: str,
    records_count: int = 0,
    details: Optional[List[Any]] = None,
    names: Optional[List[Any]] = None,
):
    db = SessionLocal()
    try:
        details_json = json.dumps(details) if details else "[]"
        names_json = json.dumps(names) if names else "[]"

        log = RequestLog(
            document=document,
            status=status,
            records_count=records_count,
            details=details_json,
            names=names_json,
        )
        db.add(log)
        db.commit()
    finally:
        db.close()


def get_total_requests():
    db = SessionLocal()
    try:
        return db.query(RequestLog).count()
    finally:
        db.close()
