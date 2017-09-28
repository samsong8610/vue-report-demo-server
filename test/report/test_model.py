import unittest

import mock

from report.model import Report

class ReportTest(unittest.TestCase):
    tmpl_str = """
    {
        "id": 1,
        "title": "test_parse",
        "layout": "linear-layout",
        "components": [
            {
                "type": "ve-line",
                "options": {
                    "data": "http://host/api/"
                }
            },
            {
                "type": "ve-line",
                "options": {
                    "data": {
                        "key": "value"
                    }
                }
            }
        ]
    }
    """

    def test_parse(self):
        inst = Report.parse(self.tmpl_str)
        self.assertIsNotNone(inst)
        self.assertEqual(1, inst.id)
        self.assertEqual('test_parse', inst.title)
        self.assertEqual('linear-layout', inst.layout)
        self.assertEqual(2, len(inst.components))
        self.assertEqual('ve-line', inst.components[0].name)

    def test_render(self):
        inst = Report.parse(self.tmpl_str)
        with mock.patch.object(inst.components[0], 'load_data') as mock_load_data:
            mock_load_data.return_value = {}
            result = inst.render()
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            mock_load_data.assert_called_once_with()
        pass

    @mock.patch('report.component.urllib2')
    def test_render_load_data_raise_exception(self, mock_urllib2):
        inst = Report.parse(self.tmpl_str)
        mock_urllib2.urlopen.side_effect = Exception('mock exception')
        with self.assertRaises(Exception):
            inst.render()
        mock_urllib2.urlopen.assert_called_once_with('http://host/api/')

    @mock.patch('report.component.urllib2')
    def test_render_load_data_not_200(self, mock_urllib2):
        inst = Report.parse(self.tmpl_str)
        resp = mock.Mock()
        resp.code = 404
        mock_urllib2.urlopen.return_value = resp
        with self.assertRaises(Exception):
            inst.render()
        mock_urllib2.urlopen.assert_called_once_with('http://host/api/')