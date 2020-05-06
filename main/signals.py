"""signals.py - собрание функций, привязанных к изменениям моделей django"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_registration.signals import user_registered

from main.models import WikiPage, UserProfile
from main.tasks import markdown_convert


@receiver(post_save, sender=WikiPage)
def wiki_post_save_callback(**kwargs):
    """Отсылка markdown-кода на преобразование в html-код в момент сохранения модели"""
    instance = kwargs['instance']
    markdown_convert.delay(id=instance.id, md_text=instance.text_markdown)


@receiver(user_registered)
def user_profile_creation(user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()
