from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

class TestDjangoConfigTest(TestCase):
    def test_secret_key_strenghth(self):
        SECRET_KEY = settings.SECRET_KEY
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            msg = f'项目SECRET_KEY{SECRET_KEY}不够安全，{e.messages}'
            self.fail(msg)