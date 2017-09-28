# -*-encoding: utf-8 -*-
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import Response


bp = Blueprint('data', __name__, template_folder='templates/data')

raw_data = [
    {
        'dataset': [
            ['1月1日', 1523, 1523, 0.12, 100],
            ['2月1日', 1223, 1523, 0.345, 100],
            ['3月1日', 2123, 1523, 0.7, 100],
            ['4月1日', 4123, 1523, 0.31, 100],
            ['5月1日', 3123, 1523, 0.12, 100],
            ['6月1日', 7123, 1523, 0.65, 100]
        ]
    },
    {
        'dataset': [
            [5000, 0.8]
        ]
    }
]


@bp.route('/<int:id>', methods=['GET'])
def get(id):
    if id < 0 or id > len(raw_data):
        abort(400)
    return jsonify(raw_data[id]['dataset'])