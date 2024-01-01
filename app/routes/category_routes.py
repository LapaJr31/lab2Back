from flask import Blueprint, jsonify, request

category_blueprint = Blueprint('category_blueprint', __name__)

categories = []

@category_blueprint.route('/category', methods=['POST'])
def create_category():
    category = request.json
    category['id'] = len(categories) + 1
    categories.append(category)
    return jsonify(category), 201

# Додайте інші маршрути для категорій тут
