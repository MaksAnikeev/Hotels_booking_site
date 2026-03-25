# Установка
1. На сервере установить гит
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
TG_BOT_TOKEN - токен вашего бота, полученный у BotFather в ТГ
PAYMENT_UKASSA_TOKEN - токен юкассы, если будете получать платежи через юкассу

данные пустой БД в постгри, она создастся автоматически по указанным вами данным
POSTGRES_URL=postgres:
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

Пример
~~~pycon
TG_BOT_TOKEN=5012401124:AAFKCbhhGsDW3rh8mMQIJgcWOXEENU
PAYMENT_UKASSA_TOKEN=381764678:TEST:119110

POSTGRES_URL=postgres://max:Anykey@pgdb:5432/get_course_td_bot
POSTGRES_DB=get_course_td_bot
POSTGRES_USER=max
POSTGRES_PASSWORD=Anykey

SECRET_KEY='django-insecure-&3s652n^nn_l-6l_i&%mc(7$ypwcs))007q%czm48tmjif&12#'
DEBUG=False
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
ALLOWED_HOSTS=127.0.0.1,localhost,get_course_bot,nginx,84.38.180.226
BASE_MEDIA_URL=http://nginx:80
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

10. Теперь настройка сервера завершена и можно запускать установку проекта
~~~pycon
docker compose build
~~~
Итог
~~~pycon
[+] Building 2/2
 ✔ backend  Built                                                                                      0.0s
 ✔ bot      Built   
~~~
Начнутся создаваться контейнеры `pgdb, nginx, django_backend, it_bot-bot`
~~~pycon
docker compose up –d
~~~
Итог
Начнутся запускатся контейнеры `pgdb, nginx, django_backend, it_bot-bot`

Чтобы посмотреть логи в реальном времени можно набрать
~~~pycon
docker-compose logs -f booking_back_service
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
