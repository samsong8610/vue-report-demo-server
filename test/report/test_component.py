# -*- encoding: utf-8 -*-
import unittest

from report.component import VeLineComponent
from report.component import ReportParagraphComponent

class VeLineComponentTest(unittest.TestCase):
    def setUp(self):
        self.options = {
            'data': [
                [u'1月1日', 1523, 1523, 0.12],
                [u'1月2日', 1223, 1523, 0.345],
                [u'1月3日', 2123, 1523, 0.7],
                [u'1月4日', 4123, 1523, 0.31],
                [u'1月5日', 3123, 1523, 0.12],
                [u'1月6日', 7123, 1523, 0.65]
            ],
            'mapping': {
                'fields': [
                    {'index': 0, 'name': 'date', 'label': u'日期'},
                    {'index': 1, 'name': 'sales_q1', 'label': u'销售额-1季度'},
                    {'index': 2, 'name': 'sales_q2', 'label': u'销售额-2季度'},
                    {'index': 3, 'name': 'percent', 'label': u'占比'},
                ],
                'dimension': [0],
                'metrics': [1, 2, 3],
                'yAxises': [
                    {'type': 'value', 'position': 'left'},
                    {'type': 'percent', 'position': 'right', 'metrics': [3]}
                ],
                'extra': {
                    'digit': 4
                }
            },
            'extra': {
                'width': '100%'
            }
        }

    def test_render_success(self):
        target = VeLineComponent(self.options)
        comp = target.render()
        self.assertIsNotNone(comp)
        options = comp['options']
        self.assertIn('columns', options['data'])
        self.assertIn('rows', options['data'])
        self.assertListEqual([u'日期', u'销售额-1季度', u'销售额-2季度', u'占比'], options['data']['columns'])
        self.assertDictEqual({u'日期': u'1月1日', u'销售额-1季度': 1523, u'销售额-2季度': 1523, u'占比': 0.12},
                             options['data']['rows'][0])
        settings = options['settings']
        self.assertIsNotNone(settings)
        self.assertListEqual([u'日期'], settings['dimension'])
        self.assertListEqual([u'销售额-1季度', u'销售额-2季度', u'占比'], settings['metrics'])
        self.assertListEqual(['value', 'percent'], settings['yAxisType'])
        self.assertListEqual(['', ''], settings['yAxisName'])
        self.assertDictEqual({'right': [u'占比']}, settings['axisSite'])
        # extra options
        self.assertEqual('100%', options['width'])
        self.assertNotIn('width', settings)
        # extra settings
        self.assertEqual(4, settings['digit'])


class ReportParagraphComponentTest(unittest.TestCase):
    def setUp(self):
        self.options = {
            'data': [
                ['v1', 'v2']
            ],
            'mapping': {
                'fields': [
                    {'name': 'k1', 'label': 'k1'},
                    {'name': 'k2', 'label': 'k2'}
                ]
            },
            'content': '{{k1}},{{k2}}'
        }

    def test_render_success(self):
        target = ReportParagraphComponent(self.options)
        comp = target.render()
        
        self.assertIsNotNone(comp)
        options = comp['options']
        self.assertDictEqual({'k1': 'v1', 'k2': 'v2'}, options['data'])
        self.assertEqual(self.options['content'], options['content'])

    def test_render_with_formatter_success(self):
        options = {
            'data': [[0.8]],
            'mapping': {
                'fields': [
                    {'name': 'p', 'label': 'p', 'formatter': 'percent'}
                ]
            },
            'content': '{{p}}'
        }
        target = ReportParagraphComponent(options)
        comp = target.render()

        self.assertIsNotNone(comp)
        self.assertDictEqual({'p': '80%'}, comp['options']['data'])