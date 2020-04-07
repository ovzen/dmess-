from django.contrib.auth.management.commands import createsuperuser as create_su
from main.models import User, UserProfile


class Command(create_su.Command):
    def handle(self, *args, **options):
        """
        Overridden method of createsuperuser's Command.
        Additionally creates a UserProfile for created User.
        """
        super().handle(*args, **options)
        user = User.objects.last()
        user_profile = UserProfile(user=user)
        user_profile.save()
