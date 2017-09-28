import abc
import copy
import itertools
import json
import urllib2

from class_registry import ClassRegistry
from report.formatter import registry as formatters


registry = ClassRegistry()

class ReportComponent(object):
    __metaclass__ = abc.ABCMeta

    def render(self, context):
        pass


class UrlSourceComponent(ReportComponent):
    def __init__(self, options):
        super(UrlSourceComponent, self).__init__()
        if 'data' not in options:
            raise ValueError('options dict must has "data" item')
        self.options = options

    def need_load(self):
        return isinstance(self.options['data'], basestring)

    def load_data(self):
        if (not self.need_load()):
            return self.options['data']

        link = self.options['data']
        try:
            resp = urllib2.urlopen(link)
            if resp.code != 200:
                raise Exception('load data from %s failed, status = %d' %
                                (link, resp.code))
            if not self.content_type_is_json(resp):
                raise Exception('data from %s is not json content type' % link)
            body = resp.read()
            return json.loads(body)
        except Exception as e:
            raise Exception('load data from %s raises exception %s' % (link, str(e)))

    def content_type_is_json(self, resp):
        content_types = resp.headers.getheaders('content-type')
        for ctype in content_types:
            if 'json' in ctype:
                return True
        return False


@registry.register('ve-line')
class VeLineComponent(UrlSourceComponent):
    name = 've-line'

    def __init__(self, options):
        super(VeLineComponent, self).__init__(options)

    def render(self):
        result = {}
        result['component'] = self.name
        options = self.map_options()
        if 'extra' in self.options:
            for key in self.options['extra']:
                options[key] = copy.deepcopy(self.options['extra'][key])
        result['options'] = options
        return result

    def map_options(self):
        result = {}
        loaded = self.load_data()

        mapping = self.options.get('mapping', None)
        if mapping is None:
            result['data'] = loaded
        else:
            mapped_data = {}
            columns = [field['label'] for field in mapping['fields']]
            mapped_data['columns'] = columns
            mapped_data['rows'] = []
            for values in loaded:
                mapped_data['rows'].append(dict(itertools.izip(columns, values)))
            result['data'] = mapped_data
            result['settings'] = self.map_settings(mapping, columns)
        return result

    def map_settings(self, mapping, columns):
        settings = {}
        if 'dimension' in mapping:
            settings['dimension'] = [columns[i] for i in mapping['dimension']]
        
        if 'metrics' in mapping:
            settings['metrics'] = [columns[i] for i in mapping['metrics']]

        if 'yAxises' in mapping:
            types = []
            names = []
            right_metrics = []
            for axis in mapping['yAxises']:
                types.append(axis.get('type', 'value'))
                names.append(axis.get('name', ''))
                if 'metrics' in axis:
                    if axis.get('position', 'left') == 'right':
                        right_metrics += [columns[i] for i in axis['metrics']]
            settings['yAxisType'] = types
            settings['yAxisName'] = names
            settings['axisSite'] = {'right': right_metrics}

        if 'extra' in mapping:
            for key in mapping['extra']:
                settings[key] = copy.deepcopy(mapping['extra'][key])
        return settings


@registry.register('report-paragraph')
class ReportParagraphComponent(UrlSourceComponent):
    name = 'report-paragraph'

    def __init__(self, options):
        super(ReportParagraphComponent, self).__init__(options)

    def render(self):
        component = {}
        component['component'] = self.name
        component['options'] = self.map_options()
        return component

    def map_options(self):
        result = {}
        loaded = self.load_data()

        if 'mapping' in self.options:
            fields = []
            values = []
            row = loaded[0]
            for i, v in enumerate(self.options['mapping']['fields']):
                fields.append(v['label'])
                if ('formatter' in v and v['formatter'] in formatters):
                    values.append(formatters[v['formatter']](row[i]))
                else:
                    values.append(row[i])
            result['data'] = dict(itertools.izip(fields, values))
        else:
            result['data'] = loaded

        if 'content' in self.options:
            result['content'] = self.options['content']
        return result