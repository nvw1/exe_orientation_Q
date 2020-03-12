from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import *

class TestUrls(SimpleTestCase):

    def test_(self):
        url = reverse('redirect')
        self.assertEqual(resolve(url).func, redirect)





