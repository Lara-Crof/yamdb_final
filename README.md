# yamdb
Проект развернут по адресу: http://localhost:8000/redoc/
https://github.com/Lara_croft/yamdb_final/a
ctions/workflows/yamdb_workflow.yaml/badge
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
### Workflow
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:

DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
Workflow состоит из трёх шагов:

Проверка кода на соответствие PEP8
Сборка и публикация образа бекенда на DockerHub.
Автоматический деплой на удаленный сервер.
Отправка уведомления в телеграм-чат.
На сервере соберите docker-compose:

sudo docker-compose up -d --build
После успешной сборки на сервере выполните команды (только после первого деплоя):
Соберите статические файлы:
sudo docker-compose exec backend python manage.py collectstatic --noinput
Примените миграции:
sudo docker-compose exec backend python manage.py migrate --noinput
Команда для заполнения базы начальными данными (необязательно):
docker-compose exec web python manage.py loaddata fixtures.json
Создать суперпользователя Django:
sudo docker-compose exec backend python manage.py createsuperuser
Проект будет доступен по вашему IP


### Автор
Слизская Лариса