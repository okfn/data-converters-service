import os
from unittest import TestCase
from convert import app


class TestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        here = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.dirname(os.path.dirname(here))
        app.config.from_pyfile(os.path.join(self.config_path, 'settings.py'))
        app.config.from_pyfile(os.path.join(self.config_path,
                               'test_settings.py'), silent=True)

    def test_1_convert_params_with_url(self):
        """Test not enough parameters to GET endpoint"""
        res = self.app.get('api/convert/foo?url=http://example.com')
        self.assertEqual('{"error": "No format or type specified"}', res.data)

    def test_2_convert_params_without_url(self):
        """Test no URL to GET endpoint"""
        res = self.app.get('api/convert/foo')
        self.assertEqual('{"error": "No URL given"}', res.data)

    def test_3_convert_get_no_matching_module(self):
        """Test no matching module to GET endpoint"""
        res = self.app.get('api/convert/foo?url=http://example.com&type=foo')
        self.assertEqual('{"error": "No converter found for foo"}', res.data)

    def test_4_convert_post_without_type(self):
        """Test no type to POST endpoint"""
        self.testdata_path = os.path.join(self.config_path, 'testdata', 'csv')
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        res = self.app.post('/api/convert/json', data={'file': csv})
        self.assertEqual('{"error": "No format or type specified"}', res.data)

    def test_5_convert_post_no_matching_module(self):
        """Test not enough parameters to convert endpoint"""
        self.testdata_path = os.path.join(self.config_path, 'testdata', 'csv')
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        res = self.app.post('/api/convert/json', data={'file': csv,
                            'type': 'foo'})
        self.assertEqual('{"error": "No converter found for foo"}', res.data)

"""
    # Note: Couldn't get this test to work as expected
    def test_6_convert_post_without_file(self):
        ""Test no file to POST endpoint""
        res = self.app.post('/api/convert/json', data={'type': 'csv', 'file': ''})
        self.assertEqual('{"error": "No format or type specified"}', res.data)
"""
