# Market

Практика создания маркета

## TODO
---

1. Реферальная система
    - При регистрации пользователя по реферальной ссылке, мы добавляем этого реферала пользователю
    - Отображение реферралов в кабинете
    - Генерация реферальной ссылки с возможностью обновления
    - Бонусная программа

    - У пользователя может быть множество рефералов

2. Доработка webpack билдера или замена на Vite, gulp


## Цели

---
1. ~~Создание разных групп пользователей и их разделение~~
2. ~~Создание дешборда~~
    - ~~Форма обновление аватара пользователя~~
    - ~~Форма обновление аватара ajax~~
    - ~~Форма обновление информации о пользователе~~
    - Test validators
3. ~~Вход при помощи metamask~~
    - Test MetamaskLoginTests
4. ~~Статические страницы~~
    - ~~Добавление app pages + Тестирование~~
    - ~~Редактирование статики в админе~~
5. Реферальная система
6. Создание маркета
    - Конвертация цены на лету
    - Таксация товара продавца
    - Интеграция с разными платежными шлюзами
        - crypto
        - stripe
        - сбер
        - yoomoney
        - qiwi
7. Создание CRM на основе маркета
8. Переход на DRF
9. Тренировка Vue
10. Тренировка github/gitlab CI


## Модели

```mermaid
---
title: Модели
---
classDiagram
    Market <|-- Category
    Category <|-- Lot

    class Market {
        title
        description = TextField
        help_description = TextField
        help_seller = TextField
        poster
    }

    class Category {
        market = ForeignKey
        lot_type = [multiple, form]
    }

    class Lot {
        user = ForeignKey
        category = ForeignKey
        -
        platform = [pc, ios, android]
        char_level
        lang = [en, ru]
        description
        short_description
        price
        price_unit
        currency = [rub,usd]
        quantity
        is_active
        deactive_after_sell

    }

    class LotLeague {
        platform
    }

    class LotType {

    }

    class User {
    }

```
