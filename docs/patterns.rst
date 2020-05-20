Паттерны проектирования, используемые в dmess
=============================================

--------------------------------
**MVT, или Model-View-Template**
--------------------------------

Паттерн, используемый в django. Представляет собой набор
моделей (models), представлений (views) и шаблонов (templates).

Основан на паттерне MVC (Model-View-Controller).

Как работает схема MVC?

- Модель (Model) предоставляет данные и реагирует на команды контроллера, изменяя своё состояние.
- Представление (View) отвечает за отображение данных модели пользователю, реагируя на изменения модели.
- Контроллер (Controller) интерпретирует действия пользователя, оповещая модель о необходимости изменений.

Model в MVT соответствует таковая в MVC, View соответствует
Controller, а Template - View.

Подробнее:

- https://ru.wikipedia.org/wiki/Model-View-Controller
- https://docs.djangoproject.com/en/3.0/#the-model-layer

В dmess он представлен файлами models.py и views.py, две пары
которых находятся в папках **admin/** и **main/**, а также папкой
**templates/** в корне проекта.

-------------------------
**Декоратор (Decorator)**
-------------------------

Структурный паттерн проектирования, который позволяет
динамически добавлять объектам новую функциональность,
оборачивая их в полезные «обёртки».

Подробнее: https://refactoring.guru/ru/design-patterns/decorator

В языке Python существует особый синтактис для «оборачивания»
функций с помощью функций-декораторов.

Пример:

.. code-block:: python3

    @decorate_function
    def function(*args, **kwargs):
        # Тело декорируемой функции

    # Декорирующая функция (декоратор)
    def decorate_function(func):
        # Функция-обёртка
        def wrapper():
            print('До вызова функции')
            func()
            print('После вызова функции')
        return wrapper

В dmess используются как стандартные декораторы из python
(**@classmethod** в классе :class:`MyTokenObtainPairSerializer`,
файл serializers.py), так и, например, декораторы из
django rest framework (**@action** в классах :class:`CountModelMixin`,
:class:`UserViewSet` и :class:`DialogViewSet`, файл views.py).
