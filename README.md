Проект YaMDb

Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

git clone <https://github.com/Talgatovich/api_yamdb>
api_yamdb
Cоздать и активировать виртуальное окружение:

python3 -m venv env (python -m venv venv)
source env/bin/activate (source venv/Scripts/activate)

Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip (python -m pip install --upgrade pip)
pip install -r requirements.txt

Выполнить миграции:

python3 manage.py migrate (python manage.py migrate)

Для заполнения базы:
Запустить скрипт "myscript" (./myscript),
Ввести в консоль ".read for_script"

Запустить проект:

python3 manage.py runserver (python manage.py runserver)
