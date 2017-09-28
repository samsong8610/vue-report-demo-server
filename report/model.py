import json

from report.component import registry

class Report(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.layout = None
        self.components = []

    @classmethod
    def parse(klazz, template):
        try:
            tmpl = json.loads(template)
        except Exception as e:
            print('Parse template failed: %s' % e)
            raise e
        instance = klazz(tmpl['id'], tmpl['title'])
        instance.layout = tmpl['layout']
        for each in tmpl['components']:
            if 'type' not in each or registry.get_class(each['type']) is not None:
                comp = registry.get(each['type'], each.get('options', None))
                instance.components.append(comp)
        return instance

    def render(self):
        result = {'id': self.id, 'title': self.title, 'layout': self.layout}
        result['components'] = [each.render() for each in self.components]
        return result