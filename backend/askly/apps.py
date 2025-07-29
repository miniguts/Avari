from django.apps import AppConfig


class AsklyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'askly'

    def ready(self):
        from .models import QuestionAnswer
        QuestionAnswer.objects.all().delete()
