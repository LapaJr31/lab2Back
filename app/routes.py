from flask import Blueprint, request, jsonify
from .extensions import db
from schemes import CurrencySchema, CategorySchema, RecordSchema, UserSchema
from .models import MoneyModel, AccountUserModel, ExpenditureCategoryModel, FinanceRecordModel
import uuid
from datetime import datetime

main_routes = Blueprint("main", __name__)

categorySchema = CategorySchema()
currencySchema = CurrencySchema()
recordSchema = RecordSchema()
userSchema = UserSchema()


# Користувачі
@main_routes.route("/user", methods=["POST"])
def create_user():
    data = userSchema.load(request.json)
    user = AccountUserModel(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


@main_routes.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = AccountUserModel.query.get(user_id)
    return jsonify(UserSchema.dump(user)), 200



@main_routes.route("/users", methods=["GET"])
def get_users():
    users = AccountUserModel.query.all()
    return jsonify(UserSchema.dump(users, many=True))


@main_routes.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = AccountUserModel.query.get(user_id)
    db.session.delete(user)
    db.sessionession.commit()
    return jsonify(UserSchema.dump(user)), 200


# Категорії
@main_routes.route("/category", methods=["POST"])
def create_category():
    category_data = request.get_json()
    data = CategorySchema.load(category_data)
    data['id'] = str(uuid.uuid4())
    category = ExpenditureCategoryModel(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict())


@main_routes.route("/category", methods=["GET"])
def get_category():
    categories = ExpenditureCategoryModel.query.all()
    return jsonify(CategorySchema.dump(categories, many=True)), 200


@main_routes.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = ExpenditureCategoryModel.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(CategorySchema.dump(category)), 200
    

# Записи
@main_routes.route("/record", methods=["POST"])
def create_record():
    record_data = request.json
    data = RecordSchema.load(record_data)

    data['record_id'] = uuid.uuid4().hex
    data['time_stamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    record = FinanceRecordModel(
        record_id=data['record_id'],
        amount_spent=data['cost_amount'],
        category_id=data['category_id'],
        user_id=data['user_id'],
        time_stamp=data['time_stamp'],
        currency_id=data['currency_id']
    )
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        return jsonify(error=str(e)), 400
    return jsonify(record.convert_to_dict()), 200


@main_routes.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if user_id is None and category_id is None:
        return "Missing parameters", 400

    query = FinanceRecordModel.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    if category_id is not None:
        query = query.filter_by(category_id=category_id)
    records = query.all()
    return jsonify(RecordSchema.dump(records, many=True)), 200

@main_routes.route('/record/<record_id>', methods=["GET"])
def get_record(record_id):
    record = FinanceRecordModel.query.get(record_id)
    return jsonify(RecordSchema.dump(record)), 200
    

@main_routes.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    global records
    record = next((record for record in records if record["id"] == record_id), None)
    if not record:
        return jsonify({"message": "Record not found"}), 404

    records = [record for record in records if record["id"] != record_id]
    return jsonify({"message": "Record deleted successfully"}), 200


#Currency

@main_routes.route('/currency', methods=["POST"])
def create_currency():
    currency_data = request.get_json()
    data = CurrencySchema.load(currency_data)
    data['id'] = str(uuid.uuid4())
    currency = MoneyModel(**data)
    try:
        db.session.add(currency)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(currency.to_dict())


@main_routes.route('/currencies', methods=["GET"])
def get_all_currency():
    currencies = MoneyModel.query.all()
    return jsonify(CurrencySchema.dump(currencies, many=True)), 200


@main_routes.route('/currency/<currency_id>', methods=["DELETE"])
def delete_currency(currency_id):
    if not uuid.UUID(currency_id, version=4):
        return jsonify({"error": "Invalid currency_id format"}), 400

    currency = MoneyModel.query.get(currency_id)
    db.session.delete(currency)
    db.session.commit()
    return jsonify(CurrencySchema.dump(currency)), 200
