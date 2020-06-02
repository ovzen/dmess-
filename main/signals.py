"""signals.py - собрание функций, привязанных к изменениям моделей django"""
from django.dispatch import receiver

from django.db.models.signals import post_save
from rest_registration.signals import user_registered

from main.models import WikiPage, UserProfile, User, Message
from admin.models import Invite, InviteAlreadyUsed
from main.serializers import DialogSerializer

from main.tasks import markdown_convert
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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


@receiver(post_save, sender=Message)
def dialog_ws_notification(**kwargs):
    dialog = kwargs['instance'].dialog
    for user in dialog.users.all():
        send_notification(user, dialog)


def send_notification(user, dialog):
    group_name = f'dialogs_user_{user.id}'
    serializer = DialogSerializer(dialog)
    channel_layer = get_channel_layer()
    content = {
        'action': 'update',
        'data': serializer.data
    }

    content = normalize_uuid(content)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notify',
            'content': content
        }
    )


def normalize_uuid(content):
    """В redis_layer есть баг, из-за чего не сериализуется UUID"""
    content['data']['id'] = str(content['data']['id'])
    content['data']['last_message']['dialog'] = str(content['data']['last_message']['dialog'])
    return content
