====================================
Создание новой страницы в режиме SPA
====================================

Как добавлять страницу в режиме SPA
-----------------------------------


1. Открыть папку /Проект/frontend/src/AdminUI/components для создания новой страницу для админов или /Проект/frontend/src/UserUI/components для создания компонента для пользователей
2. Копировать файл Example, а после переименовать его в название нового компонента
3. Изменить его как вам хочется
4. открыть /Проект/frontend/src/AdminUI/ или /Проект/frontend/src/UserUI/ и открыть файл router.js
5. В начале файла импортировать файл вашего компонента по примеру

`import Страница from './components/Ваш компонент.vue'`

6. В файле router.js добавить в массив `routes` ваш компонент по данному примеру. Внимание на кавычки!

.. code-block:: js

    {
        path: 'Путь до вашего компонента',
        name: 'Название компонента',
        component: Ваш компонент,
    }
