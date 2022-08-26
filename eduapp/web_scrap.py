import json
import os
import requests
from pprint import pprint
from eduapp.scrap import getComments
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from eduapp.nlp import sample_analyze_sentiment, sample_extract_key_phrases
from youtube_transcript_api import YouTubeTranscriptApi
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
import random
import numpy as np


class Video:
    def __init__(self, video_title=None, video_description=None, thumbnail_url=None, creator=None,
                 is_accessible_for_free=None, video_url=None, video_sample_url=None, video_iframe=None,
                 views_count=None, is_new=None, source=None, comments=(), score=None, content_match=0,
                 quality_score=0,nlp_score = 0):
        self.video_title = video_title
        self.video_description = video_description
        self.thumbnail_url = thumbnail_url
        self.creator = creator
        self.is_accessible_for_free = is_accessible_for_free
        self.video_url = video_url
        self.video_sample_url = video_sample_url
        self.video_iframe = video_iframe
        self.views_count = views_count
        self.is_new = is_new
        self.source = source
        self.video_id = None
        self.comments = comments
        self.score = score
        self.key_phrases = []
        self.overall_score = (content_match+quality_score+nlp_score)/3

    def get_score(self):
        youtube_service = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_API_KEY1'))
        video_stats = youtube_service.videos().list(
            part='statistics',
            id=self.video_id
        ).execute()['items']
        likes_count = int(video_stats[0]['statistics']['likeCount'])
        views_count = int(video_stats[0]['statistics']['viewCount'])
        comments_count = int(video_stats[0]['statistics']['commentCount'])
        sentimentObjs = sample_analyze_sentiment(self.comments)
        positiveComments, negativeComments, neutralComments = 0, 0, 0
        for comment in sentimentObjs:
            print(comment)
            if comment.sentiment == 'positive':
                positiveComments += 1
            elif comment.sentiment == 'negative':
                negativeComments += 1
            else:
                neutralComments += 1
        self.score = (positiveComments - negativeComments) / (
                positiveComments + negativeComments + neutralComments)
        self.score *= 100
        self.score += (likes_count / views_count) * 100
        if self.score < 10:
            print(self.score)
        self.score = min(self.score, 97.32 - random.uniform(3, 5))
        self.score = round(self.score, 2)
        return self.score

    def getCaptions(video_id):
        captions = []
        for value in YouTubeTranscriptApi.get_transcript(video_id, languages=['en']):
            captions.append(value['text'])
        return captions


def getWebVideos(search_query, count=20):
    videos = []
    subscriptionKey = "a78707d28759452689f0c4c90cc3b489"
    endpoint = "https://api.bing.microsoft.com/" + "/v7.0/videos/search"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscriptionKey
    }
    params = {
        "q": search_query,
        "count": str(count)
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        for video_obj in response.json()['value']:
            video_title = video_obj['name']
            video_description = video_obj['description']
            thumbnail_url = video_obj['thumbnailUrl']
            video_source = video_obj['publisher'][0]['name']
            creator = video_obj['creator']['name']
            is_accessible_for_free = video_obj['isAccessibleForFree']
            video_url = video_obj['contentUrl']
            if 'motionThumbnailUrl' in video_obj:
                video_sample_url = video_obj['motionThumbnailUrl']
            else:
                video_sample_url = None
            video_iframe = video_obj['embedHtml']
            views_count = video_obj['viewCount']
            is_new = video_obj['isSuperfresh']
            videos.append(
                Video(video_title, video_description, thumbnail_url, creator, is_accessible_for_free, video_url,
                      video_sample_url, video_iframe, views_count, is_new, video_source.lower()))
            if videos[-1].source == 'youtube':
                video_id = videos[-1].video_url.split('v=')[-1]
                videos[-1].comments = getComments(video_id)
                videos[-1].video_id = video_id
                try:
                    videos[-1].key_phrases = sample_extract_key_phrases(videos[-1].comments)
                except:
                    pass
        videos = list(filter(lambda x: x.source == 'youtube', videos))
    except Exception as ex:
        raise ex
    return videos

print(Video.getCaptions("t8pPdKYpowI"))
if __name__ == "__main__":
    # print(getWebVideos("python tutorial"))
    pass
