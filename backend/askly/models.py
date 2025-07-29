from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.constants import FORMAT_MAX_LENGTH, SOURCE_MAX_LENGHT, URL_MAX_LENGTH


class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    embedding = ArrayField(models.FloatField())
    source = models.CharField(max_length=SOURCE_MAX_LENGHT)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.question


class PromptTemplate(models.Model):
    prompt = models.TextField()
    url = models.URLField(
        max_length=URL_MAX_LENGTH,
        blank=True, null=True
    )
    format = models.CharField(max_length=FORMAT_MAX_LENGTH, default='text')
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.valid:
            PromptTemplate.objects.exclude(pk=self.pk).update(valid=False)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.prompt[:50]
