# Market

Практика создания маркета

## Цели

---
1. ~~Создание разных групп пользователей и их разделение~~
2. Создание маркета
    - Конвертация цены на лету
    - Таксация товара продавца
    - Интеграция с разными платежными шлюзами
        - stripe
        - сбер
        - yoomoney
        - qiwi
3. Создание CRM на основе маркета
4. Переход на DRF
5. Тренировка Vue
6. Тренировка github/gitlab CI


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
