"""apps.py - хранилище конфигов приложений"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    name = 'chat'


class MainAppConfig(AppConfig):
    """Основной конфиг приложения main"""
    name = 'main'

    def ready(self) -> None:
        """Импортируем модуль сигналов для того, чтобы заработало отслеживание изменений в модели"""
        import main.signals
