import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def sample_extract_key_phrases(key_word,articles) -> None:
    articles_that_mention_microsoft = []
    endpoint = "https://sihedsweep.cognitiveservices.azure.com/"
    key = "f83a533f9e974daf8cd5e3ca3f2c7560"
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = text_analytics_client.extract_key_phrases(articles)
    for idx, doc in enumerate(result):
        if not doc.is_error:
            print("Key phrases in article #{}: {}".format(
                idx + 1,
                ", ".join(doc.key_phrases)
            ))
            if key_word in doc.key_phrases:
                articles_that_mention_microsoft.append(str(idx + 1))

    print(
        "The articles that mention keyword are articles number: {}.".format(
            ", ".join(articles_that_mention_microsoft)
        )
    )



def sample_analyze_sentiment(documents):
    endpoint = "https://sihedsweep.cognitiveservices.azure.com/"
    key = "f83a533f9e974daf8cd5e3ca3f2c7560"
    if not documents:
        documents = ['good']
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
    sample_extract_key_phrases('Python',articles = [
        """
        Whether you're new to programming or an experienced developer, it's easy to learn and use Python.
        """,
        """
        a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language.
        """,
        """
        Documentation for Python's standard library, along with tutorials and guides, are available online.
        """
    ])
