# Market

Практика создания маркета

## TODO
---

1. Обновление формы регистрации
    - ~~обновление регистрационной формы~~
    - ~~обновление формы для входа~~
    - ~~Изменение урлов для логина/регистрации~~
    - ~~интеграция верстки форм~~
    - Рефактор users app => accounts
    - Избавиться от crispy-forms
    - интеграция верстки дешборда
    - новые поля у пользователя


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
