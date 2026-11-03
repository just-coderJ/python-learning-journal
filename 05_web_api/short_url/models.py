from sqlalchemy import Integer, Column, String
from database import Base

class URLItem(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    short_code = Column(String, index=True)