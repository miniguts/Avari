import markdown
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .embeddings import find_similar_question_embedding, normalize_text
from .genai_service import generate_answer, get_embedding, get_current_prompt
from .models import QuestionAnswer


class AskQuestionAPIView(APIView):
    def post(self, request):
        question = request.data.get('question')

        if not question or not isinstance(question, str):
            return Response(
                {'error': "Поле 'question' обязательно и должно быть строкой"},
                status=status.HTTP_400_BAD_REQUEST
            )

        similar_qa = find_similar_question_embedding(question)
        if similar_qa:
            return Response({
                'answer': similar_qa.answer,
                'source': 'database',
            })

        dialog_history = request.session.get('dialog_history', [])

        dialog_history.append({'role': 'user', 'content': question})

        prompt = get_current_prompt()

        context = ''
        for entry in dialog_history:
            context += (f"\n{entry['role'].capitalize()}:"
                        f" {entry['content']}")

        answer = generate_answer(
            context + f'\n\nВопрос: {question}\nОтвет:', prompt
            )

        dialog_history.append({'role': 'assistant', 'content': answer})

        request.session['dialog_history'] = dialog_history

        answer_html = markdown.markdown(answer)

        question_embedding = get_embedding(normalize_text(question))

        QuestionAnswer.objects.create(
            question=normalize_text(question),
            answer=answer_html,
            embedding=question_embedding,
            valid=True,
            source='genai'
        )

        return Response({
            'answer': answer_html,
            'source': 'genai',
        }, status=status.HTTP_201_CREATED)


def chat_page(request):
    return render(request, 'chat.html')
