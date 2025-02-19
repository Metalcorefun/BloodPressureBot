# Прототип чат-бота для измерения артериального давления

[![Python](https://img.shields.io/badge/python-3.13-blue?logo=python)](https://www.python.org/downloads/release/python-3132/)
[![aiogram](https://img.shields.io/badge/aiogram-408ff7?logo=telegram&logoColor=fff)](https://aiogram.dev/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-c93a2c?logo=sqlalchemy&logoColor=fff)](https://aiogram.dev/)
[![pydantic](https://img.shields.io/badge/pydantic-99002e?logo=pydantic&logoColor=fff)](https://aiogram.dev/)
[![alembic](https://img.shields.io/badge/alembic-c93a2c)](https://aiogram.dev/)
[![apscheduler](https://img.shields.io/badge/apscheduler-gray)](https://aiogram.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

Бот написан на python 3.13 с использованием aiogram, sqlalchemy, pydantic, alembic, apsheduler и SQLite и предназначен для удобного сбора данных об артериальном давлении.

## Фичи на данный момент
* Сбор измерений артериального давления и их сохранение в БД бота.
* Возможность выгрузки истории измерений в CSV.
* Возможность настройки оповещений от бота в нужное Вам время по МСК.
* Автоматическая инициализация и обновление БД при запуске с помощью sqlalchemy+alembic.
* Возможность развертывания с помощью Docker.

## Что можно докрутить и улучшить
* Переход на inline-клавиатуру для лучшего UX.
* Настройка оповещений не только в конкретное время, но и с заданной периодичностью.
* Реализация возможности выгрузки истории не только в CSV, но и в виде интерактивного графика (например HTML из plotly).
* Запилить админку.
* Разнообразить оповещения (сделать возможность случайных оповещений и оповещений с мемами, если юзер захочет :D)