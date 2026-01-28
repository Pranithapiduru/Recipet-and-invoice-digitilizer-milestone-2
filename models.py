from sqlalchemy import Column, String, Float
from database.db import Base

class Receipt(Base):
    __tablename__ = "receipts"

    bill_id = Column(String, primary_key=True, index=True)
    vendor = Column(String)
    date = Column(String)
    amount = Column(Float)
    tax = Column(Float)
