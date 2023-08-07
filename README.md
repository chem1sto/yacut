# **Проект YaCut | Сервис укорачивания ссылок**
## **Описание**
Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.

## Пользовательский интерфейс сервиса — одна страница с формой. Эта форма состоит из двух полей:
- обязательного для длинной исходной ссылки;
- необязательного для пользовательского варианта короткой ссылки.

***
Пользовательский вариант короткой ссылки не должен превышать 16 символов.
Если пользователь предложит вариант короткой ссылки, который уже занят, то уведомление сообщит об этом. Существующая в базе ссылка остается неизменной.
Если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис сгенерирует её автоматически. Формат для ссылки по умолчанию — шесть случайных символов, в качестве в которых использованы:
- большие латинские буквы,
- маленькие латинские буквы,
- цифры в диапазоне от 0 до 9.
> Автоматически сгенерированная короткая ссылка добавляется в базу данных, но только если в ней уже нет такого же идентификатора. В противном случае генерируется идентификатор заново.
--- 
![screenshot of sample](https://pictures.s3.yandex.net/resources/S01_131_1649172105.png)

> Примеры запросов к API, варианты ответов и ошибок приведены в спецификации *openapi.yml*

## **Автор**
Владимир Васильев | [chem1sto](https://github.com/chem1sto)

## **Техно-стек**
- Python 3.10.6
- SQLAlchemy 1.4.29
- Flask 2.0.2
- Flask-migrate 3.1.0
- Alembic 1.7.5
- Flask-wtf 1.0.0
- Flask-sqlalchemy 2.5.1


## **Как запустить проект:**
1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:chem1sto/yacut.git
```
```
cd yacut
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
```
* Если у вас Linux/MacOS
    ```bash
    source venv/bin/activate
    ```

* Если у вас windows
    ```bash
    source venv/scripts/activate
    ```
3. Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
4. Создайте БД по сценарию **migrations/** и запустите приложение:
```bash
flask db upgrade && flask run
```
Сервер Flask запустит приложение по адресу http://127.0.0.1:5000.
