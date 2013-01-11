import os
from unittest import TestCase
from convert import app


class TestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        here = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.dirname(os.path.dirname(here))
        app.config.from_pyfile(os.path.join(self.config_path, 'settings.py'))
        app.config.from_pyfile(os.path.join(self.config_path, 'test_settings.py'),
                               silent=True)

    def test_1_convert_params_with_url(self):
        """Test not enough parameters to convert endpoint"""
        res = self.app.get('api/convert/foo?url=htto://example.com')
        self.assertEqual('{"error": "No format or type specified"}', res.data)

    def test_1_convert_params_without_url(self):
        """Test not enough parameters to convert endpoint"""
        res = self.app.get('api/convert/foo')
        self.assertEqual('{"error": "No URL given"}', res.data)

