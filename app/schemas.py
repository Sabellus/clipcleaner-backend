from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    uid: str
    token: str
    country: str

class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)  # позволяем передавать python-имена

    uid: str
    country: str
    created_at: datetime = Field(serialization_alias="createdAt")
    last_seen:  datetime = Field(serialization_alias="lastSeen")

class PaymentCreate(BaseModel):
    user_uid: str
    amount: float
    description: str
    return_url: str
    idempotence_key: str

class PaymentResponse(BaseModel):
    payment_url: str
    payment_id: str
    status: str