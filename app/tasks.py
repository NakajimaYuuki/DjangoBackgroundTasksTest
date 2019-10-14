from background_task import background

from app.models import Emotion


@background(queue='honnne', schedule=5)
def honne(emotion: str):
    _honne(emotion)


def _honne(emotion: str):

    Emotion.objects.create(emotion=emotion)
