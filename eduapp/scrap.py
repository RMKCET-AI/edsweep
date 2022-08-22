import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

class Videos:
    def __init__(self,video_id,title,type = None,thumbnail = None):
        self.video_id = video_id
        self.title = title
        self.type = type
        self.thumbnail = thumbnail
        self.comments = []


def getVideos(search_query):
    youtube_service = build('youtube', 'v3', developerKey='AIzaSyDfmfiL6GTPfQCruZiVahJ74FOp1vWEVCc')
    search_response = json.dumps(youtube_service.search().list(
        q=search_query,
        part='id,snippet',
        maxResults=10
    ).execute()['items'], indent=4)
    videos = []
    for item in json.loads(search_response):
        video_title = item['snippet']['title']
        video_type = item['id']['kind']
        video_thumbnail = item['snippet']['thumbnails']['medium']['url']
        if video_type == 'youtube#video':
            video_id = item['id']['videoId']
            videos.append(Videos(video_id,video_title,video_type,video_thumbnail))
            videos[-1].comments = getComments(video_id)
        #elif video_type == 'youtube#playlist':
        #    video_id = item['id']['playlistId']
        #    videos.append(Videos(video_id,video_title,video_type,video_thumbnail))
    for video in videos:
        print(video.video_id)
        print(video.title)
        print(video.type)
        print(video.thumbnail)
    return videos

def getComments(video_id):
    youtube_service = build('youtube', 'v3', developerKey='AIzaSyDfmfiL6GTPfQCruZiVahJ74FOp1vWEVCc')
    search_response = json.dumps(youtube_service.commentThreads().list(
        videoId=video_id,
        part='snippet',
        maxResults=15
    ).execute()['items'], indent=4)
    comments = []
    for item in json.loads(search_response):
        comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    return comments
if __name__ == "__main__":
    getVideos("python")
    #getComments(video_id="t8pPdKYpowI")