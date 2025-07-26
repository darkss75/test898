from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from datetime import date
from typing import Optional
import re

class MemberBase(BaseModel):
    name: str
    phone_number: str
    start_date: date
    end_date: Optional[date] = None
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^010-\d{4}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError('전화번호는 010-0000-0000 형식이어야 합니다')
        return v
    
    @model_validator(mode='after')
    def validate_dates(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValueError('종료일은 시작일보다 늦어야 합니다')
        return self

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v):
        if v is not None:
            pattern = r'^010-\d{4}-\d{4}$'
            if not re.match(pattern, v):
                raise ValueError('전화번호는 010-0000-0000 형식이어야 합니다')
        return v

class MemberResponse(MemberBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)