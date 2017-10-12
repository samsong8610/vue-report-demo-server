# -*-encoding: utf-8 -*-
import json

from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import Response

from report.model import Report

print('%s __name__ %s' % (__file__, __name__))
bp = Blueprint('report', __name__, template_folder='templates')

new_test_data = [
  {
    'id': 1,
    'title': u'上半年销售情况',
    'layout': 'linear-layout',
    'components': [
      {
        'type': 'vs-line',
        'options': {
          'data': {
            'url': 'http://localhost:5000/data/0',
            'queries': [
              {
                'name': 'date',
                'type': 'keyword',
                'label': u'日期'
              }
            ]
          },
          'mapping': {
            'fields': [
                {'name': 'date', 'label': u'日期'},
                {'name': 'sales_q1', 'label': u'销售额-1季度'},
                {'name': 'sales_q2', 'label': u'销售额-2季度'},
                {'name': 'percent', 'label': u'占比'},
                {'name': 'other', 'label': u'其他'}
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
      }
    ]
  },
  {
    'id': 2,
    'title': u'员工学历分布情况',
    'layout': 'linear-layout',
    'components': [
      {
        'type': 'report-paragraph',
        'options': {
          'data': {
            'url': 'http://localhost:5000/data/1',
          },
          'mapping': {
            'fields': [
              {'name': 'total', 'label': 'total'},
              {'name': 'bachelorPercent', 'label': 'bachelorPercent', 'formatter': 'percent'}
            ]
          },
          'content': u'目前公司员工{{total}}人，其中本科以上学历的占比{{bachelorPercent}}。'
        }
      }
    ]
  },
  {
    'id': 3,
    'title': u'季度销售情况',
    'layout': 'linear-layout',
    'components': [
      {
        'type': 've-line',
        'options': {
          'data': {
            'url': 'http://localhost:5000/data/2',
            'query': [
              {
                'name': 'quater',
                'required': True,
                'type': 'selection',
                'multiple': False,
                'label': u'季度',
                'options': [
                  {'label': u'一季度', 'value': 0},
                  {'label': u'二季度', 'value': 1},
                  {'label': u'三季度', 'value': 2},
                  {'label': u'四季度', 'value': 3}
                ]
              }
            ]
          },
          'mapping': {
            'fields': [
                {'name': 'date', 'label': u'月份'},
                {'name': 'sales', 'label': u'销售额'},
                {'name': 'percent', 'label': u'占比'}
            ],
            'dimension': [0],
            'metrics': [1, 2],
            'yAxises': [
                {'type': 'value', 'position': 'left'},
                {'type': 'percent', 'position': 'right', 'metrics': [2]}
            ],
            'extra': {
              'digit': 4
            }
          },
          'extra': {
            'width': '100%'
          }
        }
      }
    ]
  },
]

test_data = [
  {
    'id': 1,
    'title': u'员工学历分布情况',
    'template': {
      'layout': 'linear-layout',
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
      'layout': 'linear-layout',
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
  },
  {
    'id': 3,
    'title': u'上半年销售情况',
    'template': {
      'layout': 'linear-layout',
      'children': [
        {
          'component': 've-line',
          'data': {
            'data': {
              'columns': ['日期', '销售额-1季度', '销售额-2季度', '占比', '其他'],
              'rows': [
                { '日期': '1月1日', '销售额-1季度': 1523, '销售额-2季度': 1523, '占比': 0.12, '其他': 100 },
                { '日期': '1月2日', '销售额-1季度': 1223, '销售额-2季度': 1523, '占比': 0.345, '其他': 100 },
                { '日期': '1月3日', '销售额-1季度': 2123, '销售额-2季度': 1523, '占比': 0.7, '其他': 100 },
                { '日期': '1月4日', '销售额-1季度': 4123, '销售额-2季度': 1523, '占比': 0.31, '其他': 100 },
                { '日期': '1月5日', '销售额-1季度': 3123, '销售额-2季度': 1523, '占比': 0.12, '其他': 100 },
                { '日期': '1月6日', '销售额-1季度': 7123, '销售额-2季度': 1523, '占比': 0.65, '其他': 100 }
              ]
            },
            'settings': {
              'yAxis': [
                {'type': 'value'},
                {'type': 'value', 'position': 'right', 'name': '占比'}
              ],
              'metrics': ['销售额-1季度', '销售额-2季度', '占比'],
              'dimension': ['日期']
            },
            'width': '100%'
          }
        }
      ]
    }
  }
]


@bp.route('/', methods=['GET'])
def list():
    data = new_test_data
    reports = [{'id': each['id'], 'title': each['title']} for each in data]
    return jsonify(reports)

@bp.route('/<int:id>', methods=['GET'])
def get(id):
    data = new_test_data
    found = None
    for each in data:
        if each['id'] == id:
            found = each
            break
    # if found is None:
    #     abort(404)
    # report = Report.parse(json.dumps(found))
    # return jsonify(report.render())
    return jsonify(found)
