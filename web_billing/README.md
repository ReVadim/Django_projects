## junior_admission_test
Тестовое задание Python Junior    
Создать web-сервис биллинг    

Включает в себя 3 endpoint-а:
- Создание счёта
- Перевод денег между счетами
- Запрос баланса  

Данные должны храниться в PostgreSQL    

Для проверки необходимо создать БД в Postgres.    
Команды для CMD:    
```
CREATE DATABASE billing_db;    
CREATE USER billing_user WITH PASSWORD password;    
ALTER DATABASE billing_db OWNER TO billing_user;
```    
Для загрузки данных в БД используйте команду:
```manage.py loaddata```

:white_check_mark: Добавлена [schema.yml](https://github.com/ReVadim/junior_admission_test/blob/main/web_billing/schema.yml)
