import json
import os
import requests
from pprint import pprint


class Video:
    def __init__(self, video_title=None, video_description=None, thumbnail_url=None, creator=None,
                 is_accessible_for_free=None, video_url=None, video_sample_url=None, video_iframe=None,
                 views_count=None, is_new=None):
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
        self.score = 0


def getWebVideos(search_query, count=10):
    videos = []
    subscriptionKey = "864b23f082d74615ae0925a0f0bbfa69"
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
                      video_sample_url, video_iframe, views_count, is_new))
    except Exception as ex:
        print(ex)
    return videos


if __name__ == "__main__":
    print(getWebVideos("python tutorial"))
