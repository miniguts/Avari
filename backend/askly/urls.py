from django.urls import path

from .views import AskQuestionAPIView, chat_page

urlpatterns = [
    path('', chat_page, name='chat'),
    path('api/ask/', AskQuestionAPIView.as_view()),
]
