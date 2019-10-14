import json

from background_task.models import Task
from django.test import TestCase, Client

from app.models import Emotion
from app.tasks import _honne


class TestYoshi(TestCase):

    def test(self):
        client = Client()
        # ヨシ！を送る
        result = client.get('/app/', dict(q='ヨシ！'))
        # Responseがヨシ！であることを確認する
        self.assertEqual(result.content.decode('utf-8'), 'ヨシ！')

        # 非同期処理で作成するのでprocessが立ち上がっていないので処理が呼ばれず上手くいかない
        self.assertEqual(Emotion.objects.all().count(), 1)
        e = Emotion.objects.all().first()
        self.assertEqual(e.emotion, 'ヨシ')

    def test_resove(self):
        client = Client()
        result = client.get('/app/', dict(q='ヨシ！'))
        self.assertEqual(result.content.decode('utf-8'), 'ヨシ！')
        # 非同期処理を呼んだときは裏ではTaskというモデルにレコードが作られている
        tasks = Task.objects.all()
        self.assertEqual(tasks.count(), 1)
        params = json.loads(tasks[0].task_params)
        # 非同期処理を呼ぶ際のパラメーターが正しく渡っていることを確認する
        self.assertEqual(params[0][0],  'ヨシ！')


class TestHonne(TestCase):

    def test(self):
        # _honneの中のテストはここで行う。
        # 登録されていることを確認する
        _ = _honne('ヨシ！')
        e = Emotion.objects.all().first()
        self.assertEqual(e.emotion, 'ヨシ！')
