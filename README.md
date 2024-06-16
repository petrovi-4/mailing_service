#Описание
Приложение [MailingService](https://github.com/petrovi-4/mailing_service.git) - это сервис рассылки для информирования и привлечения клиетов. 

С помощью этого сервиса вы можете: 
 
	- управлять клиентами для рассылок,
	- управлять списком рассылок,
	- формировать отчет о проведенных рассылкаъ,
	- устанавливать переодичность автоматической рассылки

##Технологии использованные в проекте
- Python 3.12
- Django 5.0.3
- Crontab 0.7.1
- Redis 5.0.3

## Запуск проекта
**Клонировать репозиторий:**

```
git@github.com:petrovi-4/mailing_service.git
```

**Создать и активировать виртуальное окружение:**

```
python3 -m venv env         (для Unix-систем)
source env/bin/activate     (для Unix-систем)
```
```
python -m venv env          (для Windows-систем)
env/Scripts/activate.bat    (для Windows-систем)
```

**Установка зависимостей из файла requirements.txt:**

```
python3 -m pip install --upgrade pip    (для Unix-систем)
python -m pip install --upgrade pip     (для Windows-систем)
```
```
pip install -r requirements.txt
```

**Выполнить миграции:**
```
python3 manage.py migrate   (для Unix-систем)
python manage.py migrate    (для Windows-систем)
```

**Запуск проекта:**

```
python3 manage.py runserver (для Unix-систем)
python manage.py runserver  (для Windows-систем)
```

**Перейти по адресу:**

```
http://127.0.0.1:8000
```

**Для запуска переодичных рассылок:**

```
python manage.py run
```


**Автор**  
[Мартынов Сергей](https://github.com/petrovi-4)

![GitHub User's stars](https://img.shields.io/github/stars/petrovi-4?label=Stars&style=social)
![licence](https://img.shields.io/badge/licence-GPL--3.0-green)