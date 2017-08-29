# -*-encoding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
from flask import Response


print('%s __name__ %s' % (__file__, __name__))
bp = Blueprint('report', __name__, template_folder='templates')

test_data = [
  {
    'id': 1,
    'title': u'员工学历分布情况',
    'template': {
      'component': 'linear-layout',
      'children': [
        {
          'component': 'report-paragraph',
          'data': {
            'context': {
              'total': 5000,
              'bachelorPercent': '80%'
            },
            'content': u'目前公司员工{{total}}人，其中本科以上学历的占比{{bachelorPercent}}。'
          }
        },
        {
          'component': 'chart',
          'data': {
            'title': {
              'text': u'员工学历分布图',
              'x': 'center'
            },
            'tooltip': {
              'trigger': 'item',
              'formatter': '{a} <br/>{b} : {c} ({d}%)'
            },
            'legend': {
              'orient': 'vertical',
              'left': 'left',
              'data': [u'高中', u'专科', u'本科', u'硕士', u'博士']
            },
            'series': [
              {
                'name': u'学历',
                'type': 'pie',
                'radius': '55%',
                'center': ['50%', '60%'],
                'data': [
                  {'value': 335, 'name': u'高中'},
                  {'value': 310, 'name': u'专科'},
                  {'value': 234, 'name': u'本科'},
                  {'value': 135, 'name': u'硕士'},
                  {'value': 1548, 'name': u'博士'}
                ],
                'itemStyle': {
                  'emphasis': {
                    'shadowBlur': 10,
                    'shadowOffsetX': 0,
                    'shadowColor': 'rgba(0, 0, 0, 0.5)'
                  }
                }
              }
            ]
          }
        }
      ]
    }
  },
  {
    'id': 2,
    'title': u'月度产销情况汇总',
    'template': {
      'component': 'linear-layout',
      'children': [
        {
          'component': 'b-table',
          'data': {
            'items': [
              { 'month': u'1月份', 'produced': 1, 'saled': 12 },
              { 'month': u'2月份', 'produced': 2, 'saled': 11 },
              { 'month': u'3月份', 'produced': 3, 'saled': 10 },
              { 'month': u'4月份', 'produced': 4, 'saled': 9 },
              { 'month': u'5月份', 'produced': 5, 'saled': 8 },
              { 'month': u'6月份', 'produced': 6, 'saled': 7 }
            ],
            'fields': {
              'month': { 'label': u'月份', 'sortable': True, 'class': 'text-center' },
              'produced': { 'label': u'产量（万大箱）', 'sortable': True },
              'saled': { 'label': u'销量（万大箱）' }
            }
          }
        }
      ]
    }
  }
]


@bp.route('/', methods=['GET'])
def list():
    reports = [{'id': each['id'], 'title': each['title']} for each in test_data]
    return jsonify(reports)

@bp.route('/<int:id>', methods=['GET'])
def get(id):
    found = None
    for each in test_data:
        if each['id'] == id:
            found = each
            break
    if found is None:
        abort(404)
    return jsonify(found)