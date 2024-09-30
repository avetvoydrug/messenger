# Cookie, JWT, Redis, database
- куки хранятся у пользователя в браузере и передаются с каждым запросом
    - как понял - это транспорт, а уже дальше мы выбираем стратегию доставки
- JWT не можем убить токен, пока он сам не доживёт свой цикл, хранится в браузере юзера
    - состоит из трёх частей xxx.xxx.xxx:
        - при запросах проверяем валидность подписи.
        - 1) алгоритм и тип аут
        - 2) содержимое, пароли и подобную чувствит инфу обычно не передают
        - 3) подпись (расшифровать нельзя, кодируется и декод. на бэкэнде, с помощью секретного ключа)
- redis, database надо каждый раз дёргать базу данных
    - с первым это происходит быстрее, но всё равно нужно думать как..