import abc

registry = {}

def percent(value):
    return '%d%%' % (value * 100)

registry['percent'] = percent