import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""
    api_key = None
    youtube = None

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv('YouTube_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pass
