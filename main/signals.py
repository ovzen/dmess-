"""signals.py - собрание функций, привязанных к изменениям моделей django"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from main.models import WikiPage
from main.tasks import markdown_convert


@receiver(post_save, sender=WikiPage)
def wiki_post_save_callback(**kwargs):
    """Отсылка markdown-кода на преобразование в html-код в момент сохранения модели"""
    instance = kwargs['instance']
    if not instance.text_html:
        markdown_convert.delay(id=instance.id, md_text=instance.text_markdown)
