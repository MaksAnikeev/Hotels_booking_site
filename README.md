# Backend для сайта, аналог бронирования отелей, типа "Островок". 
Использованы технологии FastAPI с патернами DTO, DataMapper и разделением на слой эндпойнтов, сервисов, репозитория. 
Также настроены тесты, работа с фоновыми задачами через celery и redis. Проект упакован в docker_compose
и развернут на внешнем сервере. Настроен CICD на GitLab

##  Установка
1. На сервере установить git
~~~pycon
sudo apt update
apt install git
~~~
2. Создать папку проекта
~~~pycon
mkdir -p project/back
cd project/back
~~~
3. Скачать проект с гитхаба
~~~pycon
git clone https://github.com/MaksAnikeev/it_bot.git .
~~~
4. Создать файл `.env` в корне проекта и прописать туда переменные окружения
Параметры созданной БД
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=

REDIS_HOST=localhost # для запуска на локале
REDIS_PORT=7379 # для запуска на локале
#REDIS_HOST=booking_redis # для запуска в контейнерах
#REDIS_PORT=6379 # для запуска в контейнерах

GOOGLE_EMAIL_PASSWORD= # для использование ручки по отправке email со своего адреса (требуется регистрация через гугл)

CORS_ORIGINS=*
#CORS_ORIGINS=http://localhost:8081,https://anikeev-maks.ru - # для работы с CORS при запросе на бекенд с фронта
#MIDDLEWARE_HOST=127.0.0.1,localhost # для работы кастомного middleware можно не раскомичивать

для авторизации 
JWT_SECRET_KEY=
JWT_ALGORITHM=
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=

Пример
~~~pycon
MODE=LOCAL

DB_HOST=localhost
#DB_HOST=booking_db
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=user
DB_PASS=12345

REDIS_HOST=localhost
REDIS_PORT=7379
#REDIS_HOST=booking_redis
#REDIS_PORT=6379

GOOGLE_EMAIL_PASSWORD=gcaxdfsfcbsmh

CORS_ORIGINS=*
#CORS_ORIGINS=http://localhost:8081,https://your-maks.ru
#MIDDLEWARE_HOST=127.0.0.1,localhost

JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a943tfsfa434caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
~~~
5. Установить `docker` и `docker compose`
Установка docker
~~~pycon
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update

apt-cache policy docker-ce

sudo apt install docker-ce
~~~
При успешном запуске увидите:
~~~pycon
sudo systemctl status docker

● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2025-04-30 17:36:56 UTC; 22s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 10629 (dockerd)
      Tasks: 7
     Memory: 43.9M
        CPU: 472ms
     CGroup: /system.slice/docker.service
             └─10629 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
~~~
Установка docker compose
~~~pycon
apt  install docker-compose

sudo apt-get install docker-compose-plugin
~~~
6Теперь настройка сервера завершена и можно запускать установку проекта
~~~pycon
docker compose build
~~~
Итог
~~~pycon
[+] Building 4/4
 ✔ pgdb Built                                                                                      0.0s
 ✔ redis     Built  
 ✔ nginx     Built  
 ✔ booking_back_service     Built   
......
~~~
Начнутся создаваться контейнеры `pgdb, nginx, booking_back_service, redis`
~~~pycon
docker compose up –d
~~~
Итог
Начнутся запускатся контейнеры `pgdb, nginx, booking_back_service, redis`

Чтобы посмотреть логи в реальном времени можно набрать
~~~pycon
docker compose logs -f booking_back_service
~~~

В проекте есть разделение на инфроструктурные контейнеры `pgdb, nginx, redis`
Их можно запустить отдельно один раз (первая команда, дальше проверки)
~~~pycon
docker compose -f docker-compose.infra.yml up –d
docker compose -f docker-compose.infra.yml ps
docker compose -f docker-compose.infra.yml logs -f pgdb
~~~
И контейнеры приложения, которые перезапускаем при изменении кода. Разделение сделано чтобы 
не тратить ресурсы на перезапуск инфроструктурных контейнеров 
~~~pycon
docker compose -f docker-compose.app.yml up –d
docker-compose -f docker-compose.app.yml logs -f booking_back_service
~~~
