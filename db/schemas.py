from pydantic import BaseModel, create_model_from_namedtuple
from datetime import datetime

class Conversion(BaseModel):
    from_currency: str
    to_currency: str
    requested_amount: int
    converted_amount: int
    
    class Config:
        orm_mode = True

class ConversionData(BaseModel):
    timestamp: datetime
    conversion:  Conversion
    
    class Config:
        orm_mode = True