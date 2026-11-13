from sqlalchemy import Column, Integer, String
from .database import Base

class ValueModel(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)