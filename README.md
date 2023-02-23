# Market

Практика создания маркета

## Цели

---
1. ~~Создание разных групп пользователей и их разделение~~
2. ~~Создание дешборда~~
    - ~~Форма обновление аватара пользователя~~
    - Множество форм на одной странице
3. Статические страницы + django-cms
4. реферальная система
5. Создание маркета
    - Конвертация цены на лету
    - Таксация товара продавца
    - Интеграция с разными платежными шлюзами
        - crypto
        - stripe
        - сбер
        - yoomoney
        - qiwi
6. Создание CRM на основе маркета
7. Переход на DRF
8. Тренировка Vue
9. Тренировка github/gitlab CI


## TODO

- Разработка моделей маркета подобие FunPay, но с разделением на покупатель/продавец


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
