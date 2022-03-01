# shop-fast-api

Для запуска сервера нужен docker и python 3.9.7
```
# Установить зависимости
pip install -r requirements.txt

# Запуск контейнера с postgresql
docker-compose -f docker-compose.yaml up

# Запуск приложения,
# --reload используется для автоматической перезагрузки приложения
# при изменениях кода
uvicorn main:app --reload
```

Это сервис для магазина, с системой пользователей и создания лотов
на продажу пользователями и компаниями (аля Wildberies, OZON - упрощённая версия этих приложений)
