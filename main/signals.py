"""signals.py - собрание функций, привязанных к изменениям моделей django"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_registration.signals import user_registered

from admin.models import Invite, InviteAlreadyUsed
from main.models import WikiPage, UserProfile, User
from main.tasks import markdown_convert


@receiver(post_save, sender=WikiPage)
def wiki_post_save_callback(**kwargs):
    """Отсылка markdown-кода на преобразование в html-код в момент сохранения модели"""
    instance = kwargs['instance']
    markdown_convert.delay(id=instance.id, md_text=instance.text_markdown)


@receiver(post_save, sender=User)
def user_profile_creation(**kwargs):
    """Создание профиля пользователя после создания пользователя"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created:
        profile = UserProfile(user=instance)
        profile.save()


@receiver(user_registered)
def user_invite_processing(user, request, **kwargs):
    """
    Применение модераторского инвайта к пользователю.
    Для применения флага is_staff в моделе пользователя, нужно отправить запрос вида
    `api/accounts/register/?invite_code=<YOUR_INVITE_CODE>`
    """
    invite_code = request.query_params.get('invite_code')
    try:
        invite = Invite.objects.get(code=invite_code)
        invite.use(user)
        invite.save()
    except Invite.DoesNotExist:
        return
    except InviteAlreadyUsed:
        return
