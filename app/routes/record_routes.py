from flask import Blueprint, jsonify, request

record_blueprint = Blueprint('record_blueprint', __name__)

records = []

@record_blueprint.route('/record', methods=['POST'])
def create_record():
    record = request.json
    record['id'] = len(records) + 1
    records.append(record)
    return jsonify(record), 201

# Додайте інші маршрути для записів тут
