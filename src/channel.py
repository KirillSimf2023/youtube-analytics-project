import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""
    __api_key = os.getenv('YouTube_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(channel['items'][0]['statistics']['viewCount'])


    def __str__(self):
        return f'{self.title} ({self.url})'


    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube


    def to_json(self, file_name):
        result_dict = {}
        result_dict['id'] = self.__channel_id
        result_dict['title'] = self.title
        result_dict['description'] = self.description
        result_dict['url'] = self.url
        result_dict['subscriber_count'] = self.subscriber_count
        result_dict['video_count'] = self.video_count
        result_dict['view_count'] = self.view_count

        with open(file_name, 'w', encoding='UTF-8') as file:
            data = json.dumps(result_dict, ensure_ascii=False)
            file.write(data)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
