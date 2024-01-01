from flask import Blueprint, jsonify, request

user_blueprint = Blueprint('user_blueprint', __name__)

users = []

@user_blueprint.route('/user', methods=['POST'])
def create_user():
    user = request.json
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user), 201

# Додайте інші маршрути для користувачів тут
