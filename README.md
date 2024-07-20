# GFinder

## Описание
GFinder - это проект для отслеживания цен на видеоигры с различных онлайн-магазинов. 
Он использует парсинг веб-страниц для сбора актуальной информации о ценах и уведомляет 
пользователей о снижении цен на интересующие их игры.

## Возможности
* Отслеживание цен на игры из нескольких источников.
* Уведомления о снижении цен через email.
* Поддержка множества платформ (Steam, PlayStation Store, Xbox Store и т.д.).
* Регулярное обновление данных о ценах.

### Установка
Требования  
* Python 3.8 или выше  
* Библиотеки:
  * requests
  * BeautifulSoup4

### Шаги установки
#### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/Och1ta/parser_game_price.git
cd parser_game_price
```

#### 2. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

#### 3. Настройте параметры проекта:

* Создайте файл .env в корневом каталоге проекта.  
* Добавьте следующие параметры в файл .env: 

```bash
SECRET_KEY = 'django-insecure-cg6*%6d51ef8f#4!r3*$vmxm4)abgjw8mo!4y-q*uq1!4$-89$'
DEBUG = 'True'
ALLOWED_HOSTS = '127.0.0.1, localhost,'
```


#### 4. Запустить проект
```bash
python main.py
```

### API
Проект включает API для работы с данными о ценах. Для удобного тестирования и проверки API, 
вы можете использовать коллекцию Postman, которая прилагается к проекту.

#### Как использовать коллекцию Postman
##### Импортируйте коллекцию Postman:

* Откройте Postman.
* Нажмите на кнопку "Import" в верхнем левом углу.
* Выберите файл GFinder.postman_collection.json из корневого каталога проекта и нажмите "Import".


