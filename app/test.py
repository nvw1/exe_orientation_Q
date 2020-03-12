# author : Nik, Hao

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import *

class TestUrls(SimpleTestCase):

    def test_(self):
        """
        Test the redirect works properly.
        """
        url = reverse('redirect')
        self.assertEqual(resolve(url).func, redirect)




