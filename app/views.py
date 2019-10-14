from django.http import HttpResponse

from app.tasks import honne


def index(request):

    param = request.GET.get('q', 'ヨシ！')

    if param == 'ヨシ！':
        honne('ヨシ！')
    else:
        honne('シらない')

    return HttpResponse('ヨシ！')
