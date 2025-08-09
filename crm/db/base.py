from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from db.database import Base
from sqlalchemy.types import TypeDecorator, TEXT
import json


class JSONEncodedList(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)


class LeadModel(Base):
    __tablename__ = "leads_data"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    email = Column(Text, unique=True, index=True)
    phone = Column(String(100), index=True)
    ip = Column(Text, index=True, nullable=False)
    password = Column(String, default='qwerty123')
    landing_url = Column(Text, index=True)
    create_at = Column(DateTime, index=True, default=datetime.now)
    status = Column(JSONEncodedList, index=True, default=['New'])
    ftd = Column(Boolean, index=True, default=False)


class AdminsModel(Base):

    __tablename__ = "admins_model"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    email = Column(Text, unique=True, index=True)
    password = Column(String)

    create_at = Column(DateTime, index=True, default=datetime.now)
    super_admin = Column(Boolean, index=True, default=True)
