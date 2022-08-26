import os
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import requests
from eduapp.nlp import sample_analyze_sentiment
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import os





class Video:
    def __init__(self, video_id, title, type=None, thumbnail=None):
        self.video_id = video_id
        self.title = title
        self.type = type
        self.thumbnail = thumbnail
        self.comments = []
        self.captions = []
        self.score = 0


def getVideos(search_query, count=10):
    youtube_service = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY1'))
    search_response = json.dumps(youtube_service.search().list(
        q=search_query,
        part='id,snippet',
        maxResults=count
    ).execute()['items'], indent=4)
    videos = []
    for item in json.loads(search_response):
        try:
            video_title = item['snippet']['title']
            video_type = item['id']['kind']
            video_thumbnail = item['snippet']['thumbnails']['medium']['url']
            if video_type == 'youtube#video':
                video_id = item['id']['videoId']
                video_stats = youtube_service.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()['items']
                likes_count = int(video_stats[0]['statistics']['likeCount'])
                views_count = int(video_stats[0]['statistics']['viewCount'])
                comments_count = int(video_stats[0]['statistics']['commentCount'])
                currVideo = Video(video_id, video_title, video_type, video_thumbnail)
                currVideo.comments = getComments(video_id)
                sentimentObjs = sample_analyze_sentiment(currVideo.comments)
                positiveComments, negativeComments, neutralComments = 0, 0, 0
                for comment in sentimentObjs:
                    if comment.sentiment == 'positive':
                        positiveComments += 1
                    elif comment.sentiment == 'negative':
                        negativeComments += 1
                    else:
                        neutralComments += 1
                currVideo.score = (positiveComments - negativeComments) / (
                        positiveComments + negativeComments + neutralComments)
                currVideo.score *= 100
                currVideo.score += (likes_count / views_count) * 100
                if currVideo.score < 10:
                    print(currVideo.score)
                currVideo.score = min(currVideo.score, 97.32)
                currVideo.score = round(currVideo.score, 2)
                if currVideo.score >= 25:
                    videos.append(currVideo)
        except:
            pass
    return videos


def getCaptions(video_id):
    captions = []
    for value in YouTubeTranscriptApi.get_transcript(video_id, languages=['en']):
        captions.append(value['text'])
    return captions


def getComments(video_id, count=10):
    youtube_service = build('youtube', 'v3', developerKey=os.environ.get("YOUTUBE_API_KEY2"))
    search_response = json.dumps(youtube_service.commentThreads().list(
        videoId=video_id,
        part='snippet',
        maxResults=count
    ).execute()['items'], indent=4)
    comments = []
    for item in json.loads(search_response):
        comments.append(
            BeautifulSoup(item['snippet']['topLevelComment']['snippet']['textDisplay'], 'html.parser').get_text())
    return comments


def getScore(video_obj, video_id):
    youtube_service = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY1'))
    video_stats = youtube_service.videos().list(
        part='statistics',
        id=video_id
    ).execute()['items']
    likes_count = int(video_stats[0]['statistics']['likeCount'])
    views_count = int(video_stats[0]['statistics']['viewCount'])
    comments_count = int(video_stats[0]['statistics']['commentCount'])
    currvideo_comments = video_obj.comments
    sentimentObjs = sample_analyze_sentiment(currVideo.comments)
    positiveComments, negativeComments, neutralComments = 0, 0, 0
    for comment in sentimentObjs:
        if comment.sentiment == 'positive':
            positiveComments += 1
        elif comment.sentiment == 'negative':
            negativeComments += 1
        else:
            neutralComments += 1
    video_obj.score = (positiveComments - negativeComments) / (
            positiveComments + negativeComments + neutralComments)
    video_obj.score *= 100
    video_obj.score += (likes_count / views_count) * 100
    if video_obj.score < 10:
        print(video_obj.score)
    video_obj.score = min(video_obj.score, 97.32)
    video_obj.score = round(video_obj.score, 2)


if __name__ == "__main__":
    # getVideos("python")
    # getComments(video_id="t8pPdKYpowI")
    # print(getCaptions(video_id="t8pPdKYpowI"))
    print()
