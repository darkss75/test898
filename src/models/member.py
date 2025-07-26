from sqlalchemy import Column, Integer, String, Date
from ..database.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)