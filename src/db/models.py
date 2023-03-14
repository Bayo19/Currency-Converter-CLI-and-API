from sqlalchemy import String, Float, Column, Integer, ForeignKey, DateTime
from db.database import Base

class Rate(Base):
    __tablename__ = "exchangerates"
    currency_code = Column(String, primary_key=True)
    rate = Column(Float)


class Portfolio(Base):
    __tablename__ = "portfolio"
    username = Column(String, unique=True)
    id = Column(Integer, primary_key=True, autoincrement=True)


class PortfolioBalance(Base):
    __tablename__ = "portfolio_balance"
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), primary_key=True)
    currency = Column(String, primary_key=True)
    amount = Column(Float)
    timestamp = Column(DateTime)
