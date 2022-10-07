# yamdb

### Краткое описание проекта
Проект представляет собой API-платформу для социальных сетей [YATUBE]). Может быть использован веб- и бэкенд-разработчиками с целью поддержки коммуникации пользователей без создания отдельного сервиса, а также для создания возможности корпоративного (группового) общения.

### Технологии
 - Python 
 - Django
 - rest-framework
 - docker
 - nginx

### Наполнение env-файла
В корневой папке создайте файл .env со следующим содержимым:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db
DB_PORT=5432
```
### Запуск проекта на локальном компьютере
- В терминале перейдите в директорию infra_sp2/infra/;
- Для сборки и запуска контейнеров выполните команду:
```
sudo docker-compose up -d
```
- Выполните миграции:
```
sudo docker-compose exec web python manage.py migrate
```
- Создайте суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
- Соберите статические файлы:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
### База данных
Для ручного заполнения базы данных перейдите в браузере по адресу:
```
http://localhost/admin/
```
Ведите данные суперпользователя и работайте на сайте администратора.
Для автоматического заполнения базы данных из файла дампа выполните следующую команду в терминале:
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

### Автор
Слизская Лариса