import os
from googleapiclient.discovery import build


class Video:
    __api_key = os.getenv('YouTube_API_KEY')
    youtube = build('youtube', 'v3', developerKey=__api_key)


    def __init__(self, id_video):
        self.id_video = id_video
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.id_video).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.id_video}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id
