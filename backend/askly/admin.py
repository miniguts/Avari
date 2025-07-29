from django.contrib import admin

from .models import PromptTemplate, QuestionAnswer


@admin.register(QuestionAnswer)
class QAEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'valid', 'created_at')
    search_fields = ('question',)

    def save_model(self, request, obj, form, change):
        if change and not form.cleaned_data.get('valid', True):
            obj.delete()
        else:
            super().save_model(request, obj, form, change)


@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'url', 'valid', 'created_at')
    search_fields = ('prompt', 'url')
    list_filter = ('valid',)
