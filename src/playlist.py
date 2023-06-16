import datetime
import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

class PlayList():

    __api_key = os.getenv('YouTube_API_KEY')
    __youtube = build('youtube', 'v3', developerKey=__api_key)


    def __init__(self, id_PlayList: str):
        '''
        Реализуйте класс PlayList, который инициализируется id плейлиста и имеет следующие публичные атрибуты:
        название плейлиста
        ссылку на плейлист
        :param id_PlayList:
        '''
        self.id_PlayList = id_PlayList
        self.url = f"https://www.youtube.com/playlist?list={id_PlayList}"
        playlist_info = self.__youtube.playlists().list(part="snippet", id=self.id_PlayList).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.current_playlist = self.get_playlist()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    @property
    def total_duration(self) -> timedelta:
        '''
        total_duration возвращает объект класса datetime.timedelta
        с суммарной длительность плейлиста
        (обращение как к свойству, использовать @property)
        :return: суммарной длительность плейлиста
        '''

        # длительность с дефолтным значением.
        duration: timedelta = timedelta(0,0,0,0,0)

        for item in self.current_playlist:
            duration += isodate.parse_duration(item['duration'])

        return duration



    def show_best_video(self) -> str:
        '''
        show_best_video() возвращает ссылку на самое популярное видео
         из плейлиста (по количеству лайков)
        :return:ссылку на самое популярное видео из плейлиста
        '''

        url_result: str = 'Нет видео в плейлисте'
        max_like: int = 0

        for item in self.current_playlist:
            if int(item['likeCount']) > max_like:
                max_like = int(item['likeCount'])
                url_result = item['url']

        return url_result

    def get_playlist(self) -> list:
        '''
        Функция получает информацию о всех виде по нашему ID плэйлиста
        :return: список словарей, с детальной информацией по каждому видео
        '''

        # итоговый список словарей о детальной информации по всем видео
        current_playlist=[]

        # получаем все видео в плейлисте
        playlist_video = self.__youtube.playlistItems().list(playlistId=self.id_PlayList,
                                                 part='contentDetails',
                                                 maxResults=50,
                                                 ).execute()

        # по каждому видео получаем детальную информацию
        for item in playlist_video['items']:
            video_details = self.__youtube.videos().list(part='contentDetails,statistics', id=item['contentDetails']['videoId']).execute()
            current_playlist.append({'id': item['contentDetails']['videoId'],
                                     "duration": video_details['items'][0]['contentDetails']['duration'],
                                     'likeCount': video_details['items'][0]['statistics']['likeCount'],
                                     'url': f"https://youtu.be/{item['contentDetails']['videoId']}"})

        return current_playlist



