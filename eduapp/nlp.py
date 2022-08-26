import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

#def


def sample_analyze_sentiment(documents):
    endpoint = "https://rmkedsweep.cognitiveservices.azure.com/"
    key = "91752d914cc947a0bed9eabbfd77100d"
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = text_analytics_client.analyze_sentiment(documents, show_opinion_mining=True)
    results = [doc for doc in response if not doc.is_error]
    for result in results:
        print(result.id, result.sentiment, result.confidence_scores)
    return results



if __name__ == "__main__":
    sample_analyze_sentiment([
        """I had the best day of my life. I decided to go sky-diving and it made me appreciate my whole life so much more.
        I developed a deep-connection with my instructor as well, and I feel as if I've made a life-long friend in her.""",
        """This was a waste of my time. All of the views on this drop are extremely boring, all I saw was grass. 0/10 would
        not recommend to any divers, even first timers.""",
        """This was pretty good! The sights were ok, and I had fun with my instructors! Can't complain too much about my experience""",
        """I only have one word for my experience: WOW!!! I can't believe I have had such a wonderful skydiving company right
            in my backyard this whole time! I will definitely be a repeat customer, and I want to take my grandmother skydiving too,
        I know she'll love it!""",
    ])
