from sqlalchemy import String, Float, Column, Integer, ForeignKey, UniqueConstraint, DateTime
from db.database import Base

# Model
class Rate(Base):

    __tablename__ = "exchangerates"
    currency_code = Column(String, primary_key=True)
    rate = Column(Float)


class Portfolio(Base):
    timestamp = Column()
    __tablename__ = "portfolio"
    username = Column(String)
    id = Column(Integer, primary_key=True)
    __table_args__ = UniqueConstraint('username')


class PortfolioBalance(Base):
    __tablename__ = "portfolio_balance"
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    currency = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime)