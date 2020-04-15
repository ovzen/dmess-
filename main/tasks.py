"""tasks.py - celery-задачи проекта"""

import markdown
from dmess.celery import app
from main.models import WikiPage


@app.task()
def markdown_convert(**kwargs):
    """Отложенное задание для преобразования markdown-поля в модели в html-код.

    Берём markdown-текст, преобразовываем в html и записываем обратно в модель
    :param kwargs: словарь с параметрами. Должен содержать ключ id (primary key в модели WikiPage)
    """
    wiki_object = WikiPage.objects.get(id=kwargs['id'])
    text_html = markdown.markdown(wiki_object.text_markdown)
    if wiki_object.text_html != text_html:
        wiki_object.text_html = text_html
        wiki_object.save()
