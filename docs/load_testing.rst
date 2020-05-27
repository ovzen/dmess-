Нагрузочное тестирование технологией Yandex Tank
================================================

Тестирование проходило при линейно возрастающей нагрузке с 1 до 200 запросов в секудну (rps) на d-messenger.ml, и пока на протяжении последних 20 секунд не будут появляться 25 ненулевых сетевых ошибкок(net_xx), заданная продолжительность - 10 минут. Тест завершился с помощью утилиты autostop при 132 rps, на 6 минуте.
Видно, что на отметке в 97 rps сайт уже не способен обрабатывать все запросы одновременно с обычным временем отклика от 400 до 440 мс.
После 96 rps количество необработанных запросов (активных потоков) увеличивается с 45 до 538, и сайт перестает отвечать на большинство запросов, вызывая ошибки net_71 (Protocol error), net_104 (Connection reset by peer) и net_110 (Connection timed out).
При этом медианное значение времени отклика - 5 секунд.

Телеметрия сервера показала, что причиной возникновения сетевых ошибок и потери пакетов является малая производительность процессора. До 90 rps процессору еще удается обработать все поступающие запросы, однако далее, не успевая ответить на один, сервер получает еще дополнительные, что приводит к резкому росту количества активных соединиений и необработанных запросов.

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
        - /auth/login/?next=%2F
      load_profile:
        load_type: rps
        schedule: line(1, 200, 10m)
      ssl: true
    autostop:
      autostop:
        - net(xx, 25, 20)
    console:
      enabled: true
    telegraf:
      config: monitoring.xml
      enabled: true
      kill_old: false
      package: yandextank.plugins.Telegraf
      ssh_timeout: 30s

**monitoring.xml**

.. code-block:: XML

  <Monitoring>
    <Host address="d-messenger.ml" interval="1" username=[username] telegraf=[path to telegraf binary]>
      <CPU/> <Kernel/> <Net/> <System/> <Memory/> <Disk/> <Netstat /> <Nstat/>
    </Host>
  </Monitoring>

Результаты опубликованы на сервисе аналитики производительности **Yandex Overload**:
https://overload.yandex.net/275692