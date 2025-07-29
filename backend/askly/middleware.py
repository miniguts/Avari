import json
import os

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SaveDialogHistoryMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        dialog_history = request.session.get('dialog_history', [])

        if dialog_history:
            self.save_dialog_history_to_file(
                request.session.session_key, dialog_history
            )

        return response

    def save_dialog_history_to_file(self, session_id, dialog_history):
        history_file = os.path.join(settings.BASE_DIR, 'dialog_history.json')

        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as file:
                existing_history = json.load(file)
        else:
            existing_history = []

        existing_history.append({
            'session_id': session_id,
            'history': dialog_history
        })

        with open(history_file, 'w', encoding='utf-8') as file:
            json.dump(existing_history, file, ensure_ascii=False, indent=4)
