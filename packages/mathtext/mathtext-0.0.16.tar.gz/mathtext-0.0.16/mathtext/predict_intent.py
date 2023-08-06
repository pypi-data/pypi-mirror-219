"""
To predict intent tags within your application, run the following:

>>> from mathtext.predict_intent import predict_message_intent
>>> predict_message_intent('Hello world message from user')
{ 
  'type': 'intent',
  'data': ... 
  'confidence': ...
  'intents': [
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
    {
      'type': 'intent',
      'data': ...
      'confidence': ...
    },
}
"""
import joblib
import pandas as pd

from mathtext.constants import (
    DATA_DIR,
    CLIENT,
    CURRENT_MODEL_FILENAME,
    CURRENT_MODEL_LINK,
    OBJECT_STORAGE_NAME,
    )
# MANDATORY imports for joblib to unpickle the model (pipeline)
from mathtext.models.multilabel_intent_recognition import (  # noqa
    BERTEncoder,
    Pipeline,
    OneVsRestClassifier,
    LogisticRegression,
    SentenceTransformer,
    BaseEstimator,
    TransformerMixin
    )

# FIXED: never define a new path within the code
#   Always reuse a previously defined path (DATA_DIR), preferably from constants.py
#   And try to avoid using Path('') or Path.cwd() so that code can run anywhere
local_model = CLIENT.download_file(
  OBJECT_STORAGE_NAME,
  CURRENT_MODEL_LINK,
  str(DATA_DIR / CURRENT_MODEL_FILENAME)
)

INTENT_RECOGNIZER_MODEL = joblib.load(DATA_DIR / CURRENT_MODEL_FILENAME)


def predict_message_intent(message, min_confidence=.5):
    """ Runs the trained model pipeline on a student's message

    >>> predict_message_intent('next') # doctest: +ELLIPSIS
    {'type': 'intent', 'data': 'next', 'confidence': 0.74...}

    >>> predict_message_intent('What do I do?')
    {'type': 'intent', 'data': 'no_match', 'confidence': 0}
    """
    pred_probas = INTENT_RECOGNIZER_MODEL.predict_proba([message])[0]

    predicted_labels_and_scores = pd.Series(
      list(pred_probas),
      index=INTENT_RECOGNIZER_MODEL.label_mapping
    )

    predictions = predicted_labels_and_scores.sort_values(ascending=False)[:3].to_dict().items()

    intents = [{'type': 'intent', 'data': name, 'confidence': conf} for name, conf in predictions]

    data = intents[0]['data']
    confidence = intents[0]['confidence']
    if confidence < min_confidence:
        data = 'no_match'
        confidence = 0

    return {
      "type": "intent",
      "data": data,
      "confidence": confidence,
      "intents": intents
    }
