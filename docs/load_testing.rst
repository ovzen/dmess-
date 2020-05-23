Нагрузочное тестирование технологией Yandex Tank
================================================

При линейно возрастающей нагрузке с 1 до 200 запросов в секудну (rps) на d-messenger.ml видно, что на отметке в 97 rps сайт не способен обрабатывать все запросы одновременно с обычным временем отклика от 381 до 420 мс.
После 97 rps количество необработанных запросов (активных потоков) увеличивается с 43 до 490, и сайт перестает отвечать на большинство запросов,
появляются ошибки net_71 (Protocol error), net_104 (Connection reset by peer) и net_110 (Connection timed out).
При этом медианное значение времени отклика - 4 секунды.

Конфигурация Яндекс Танка
-------------------------

**load.yaml**

.. code-block:: yaml

    overload:
        enabled: true
        package: yandextank.plugins.DataUploader
        token_file: "token.txt"
    phantom:
        address: d-messenger.ml:443
        headers:
            - "[Authorization: <token>]"
        uris:
            - /auth/login
        load_profile:
            load_type: rps
            schedule: line(1, 200, 7m)
        ssl: true
    console:
        enabled: true
    telegraf:
        enabled: false

Результаты опубликованы на сервисе аналитики производительности Yandex Overload:
https://overload.yandex.net/273883