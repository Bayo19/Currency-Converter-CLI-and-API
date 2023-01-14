from sqlalchemy import String, Float, Column
from db.database import Base

# Model
class Rate(Base):

    __tablename__ = "exchangerates"
    currency_code = Column(String, primary_key=True)
    rate = Column(Float)
