Запрос на создание юзера 

curl -X POST "http://localhost:8000/user" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "test_user_123",
    "country": "RU",
    "token": "super_secret_token"
  }'


Запрос на создание платежа 

curl -X POST "http://localhost:8000/payment/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_uid": "test_user_123",
    "amount": 3.00,
    "description": "Заказ №73",
    "return_url": "https://clipcleaner.app/"
  }'
