from flask import Blueprint, request, jsonify

main_routes = Blueprint("main", __name__)

users = []
categories = []
records = []


# Користувачі
@main_routes.route("/user", methods=["POST"])
def create_user():
    user_data = request.json
    user_data["id"] = len(users) + 1
    users.append(user_data)
    return jsonify(user_data), 201


@main_routes.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in users if user["id"] == user_id), None)
    return jsonify(user or {"message": "Користувач не знайдений"}), (
        200 if user else 404
    )


@main_routes.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@main_routes.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200


# Категорії
@main_routes.route("/category", methods=["POST"])
def create_category():
    category_data = request.json
    category_data["id"] = len(categories) + 1
    categories.append(category_data)
    return jsonify(category_data), 201


@main_routes.route("/category", methods=["GET"])
def get_categories():
    return jsonify(categories)


@main_routes.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    global categories
    category = next(
        (category for category in categories if category["id"] == category_id), None
    )
    if not category:
        return jsonify({"message": "Category not found"}), 404

    categories = [category for category in categories if category["id"] != category_id]
    return jsonify({"message": "Category deleted successfully"}), 200


# Записи
@main_routes.route("/record", methods=["POST"])
def create_record():
    record_data = request.json
    record_data["id"] = len(records) + 1
    records.append(record_data)
    return jsonify(record_data), 201


@main_routes.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if not user_id and not category_id:
        return jsonify({"message": "Параметри user_id та category_id обов'язкові"}), 400

    filtered_records = [
        record
        for record in records
        if record.get("user_id") == user_id and record.get("category_id") == category_id
    ]
    return jsonify(filtered_records)


@main_routes.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    global records
    record = next((record for record in records if record["id"] == record_id), None)
    if not record:
        return jsonify({"message": "Record not found"}), 404

    records = [record for record in records if record["id"] != record_id]
    return jsonify({"message": "Record deleted successfully"}), 200
