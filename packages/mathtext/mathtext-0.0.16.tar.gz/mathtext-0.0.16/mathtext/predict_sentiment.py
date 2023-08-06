from mathtext.models.sentiment_model import sentiment_model


def sentiment(text):
    """ Compute sentiment (positive/negative: 0-1) """
    return sentiment_model(text.lower())