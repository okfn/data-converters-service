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

    def test_1_convert_xls(self):
        """Test converting a XLS to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/xls/simple.xls&type=xls')
        """
        Commented out due to issue #30 in messytables
        assert ('"metadata": {"fields": [{"type": "DateTime", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        """
        assert ('"metadata": {"fields": [{"type": "String", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-01 00:00:00", "place": "Galway", '
                '"temperature": 1.0}' in res.data)

    def test_2_convert_xlsx(self):
        """Test converting a XLSX to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/xls/simple.xlsx&type=xls&'
                           'excel_type=xlsx')
        assert ('"metadata": {"fields": [{"type": "String", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-03 00:00:00", "place": "Berkeley", '
                '"temperature": 5}' in res.data)

    def test_3_post_xls_file(self):
        """Test POSTing an xls file to the API"""
        self.testdata_path = os.path.join(self.config_path, 'testdata', 'xls')
        xls = open(os.path.join(self.testdata_path, 'simple.xls'))
        res = self.app.post('/api/convert/json', data={'file': xls,
                            'type': 'xls'})
        assert ('"metadata": {"fields": [{"type": "String", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-01 00:00:00", "place": "Galway", '
                '"temperature": 1.0}' in res.data)

    def test_3_post_xlsx_file(self):
        """Test POSTing an XLSX file to the API"""
        self.testdata_path = os.path.join(self.config_path, 'testdata', 'xls')
        xls = open(os.path.join(self.testdata_path, 'simple.xlsx'))
        res = self.app.post('/api/convert/json', data={'file': xls,
                            'type': 'xls', 'excel_type': 'xlsx'})
        assert ('"metadata": {"fields": [{"type": "String", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-03 00:00:00", "place": "Berkeley", '
                '"temperature": 5}' in res.data)
