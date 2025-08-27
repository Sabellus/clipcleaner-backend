from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas, database
from .config import settings
import secrets
import uuid
from app.models import User
from app.schemas import PaymentCreate, PaymentResponse
from yookassa import Configuration, Payment
from decimal import Decimal

# Настройка конфигурации YooKassa (добавьте в config.py)
Configuration.account_id = settings.yookassa_shop_id
Configuration.secret_key = settings.yookassa_secret_key

app = FastAPI(title="Users API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user", response_model=schemas.UserResponse)
def create_or_get_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    # безопасное сравнение токена
    if not secrets.compare_digest(data.token, settings.secret_token):
        raise HTTPException(status_code=403, detail="Invalid token")

    user = db.query(models.User).filter(models.User.uid == data.uid).first()
    if user:
        # обновляем last_seen на уровне БД
        user.last_seen = func.now()
        db.add(user)
        db.commit()
        db.refresh(user)
        return schemas.UserResponse(
            uid=user.uid, country=user.country,
            created_at=user.created_at, last_seen=user.last_seen
        )

    # создаём нового
    new_user = models.User(uid=data.uid, country=data.country)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.UserResponse(
        uid=new_user.uid, country=new_user.country,
        created_at=new_user.created_at, last_seen=new_user.last_seen
    )
print(f"YooKassa config: shop_id={settings.yookassa_shop_id}, secret_key={settings.yookassa_secret_key}")
@app.post("/payment/create", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    """
    Создает платеж в YooKassa с корректным receipt
    """
    # Проверяем существование пользователя
    user = db.query(User).filter(User.uid == data.user_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        # Генерируем уникальный ключ идемпотентности
        idempotence_key = str(uuid.uuid4())
        
        # Сумма как Decimal
        amount_value = Decimal(f"{data.amount:.2f}")
        
        payment_payload = {
            "amount": {"value": amount_value, "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {"type": "redirect", "return_url": data.return_url},
            "description": data.description,
            "metadata": {"user_uid": data.user_uid},
            "receipt": {
                "customer": {"email": "nakazan.ru@gmail.com"},
                "items": [
                    {
                        "description": data.description,
                        "quantity": "1.00",
                        "amount": {"value": amount_value, "currency": "RUB"},
                        "vat_code": 1,
                        "payment_subject": "service",
                        "payment_mode": "full_payment"
                    }
                ]
            },
            "test": True
        }
        
        # Создаём платеж
        payment = Payment.create(payment_payload, idempotence_key)
        
        return PaymentResponse(
            payment_url=payment.confirmation.confirmation_url,
            payment_id=payment.id,
            status=payment.status
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")