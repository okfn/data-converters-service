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

    def test_1_convert_csv(self):
        """Test converting a CSV to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/csv/simple.csv&type=csv')
        assert ('"metadata": {"fields": [{"type": "DateTime", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-01 00:00:00", "place": "Galway", '
                '"temperature": 1}' in res.data)

    def test_2_unicode_csv(self):
        """Test converting a CSV with unicode chars to JSON"""
        res = self.app.get('/api/convert/json?url='
                           'http://resources.opendatalabs.org/u/nigelb/'
                           'data-converters/csv/spanish_chars.csv&type=csv')
        assert ('"metadata": {"fields": [{"type": "Integer", "id": "GF_ID"}, '
                '{"type": "Integer", "id": "FN_ID"}, {"type": "Integer", '
                '"id": "SF_ID"}, {"type": "String", "id": "GF"}, {"type": '
                '"String", "id": "F"}, {"type": "String", "id": "SF"}, {"type'
                '": "Float", "id": "Gasto total 2011"}, {"type": "String", '
                '"id": "Descripci\u00f3n"}]}' in res.data)
        assert ('{"Gasto total 2011": 229932.5, "F": "", "Descripci\u00f3n": '
                '" Comprende las acciones propias de la gesti\u00f3n  '
                'gubernamental, tales como la administraci\u00f3n de asuntos '
                'de car\u00e1cter legislativo,  procuraci\u00f3n e '
                'impartici\u00f3n de justicia, asuntos militares y seguridad '
                'nacional, asuntos con el exterior, asuntos hacendarios, '
                'pol\u00edtica interior, organizaci\u00f3n de los procesos '
                'electorales, regulaci\u00f3n y normatividad aplicable a los '
                'particulares y al propio sector p\u00fablico, '
                'protecci\u00f3n  y conservaci\u00f3n del medio ambiente y '
                'recursos naturales y la administraci\u00f3n interna del '
                'sector p\u00fablico.", "SF_ID": "", "GF_ID": 1, "GF": '
                '"Gobierno", "FN_ID": "", "SF": ""}' in res.data)

    def test_3_post_file(self):
        """Test POSTing a file to the API"""
        self.testdata_path = os.path.join(self.config_path, 'testdata', 'csv')
        csv = open(os.path.join(self.testdata_path, 'simple.csv'))
        res = self.app.post('/api/convert/json', data={'file': csv, 'type': 'csv'})
        assert ('"metadata": {"fields": [{"type": "DateTime", "id": "date"}, '
                '{"type": "Integer", "id": "temperature"}, {"type": "String",'
                ' "id": "place"}]}' in res.data)
        assert ('{"date": "2011-01-01 00:00:00", "place": "Galway", '
                '"temperature": 1}' in res.data)
