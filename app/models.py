from sqlalchemy import func
from .extensions import db

class MoneyModel(db.Model):
    __tablename__ = 'money_type'

    money_id = db.Column(db.String, primary_key=True)
    money_name = db.Column(db.String(128), nullable=False)

    finance_record = db.relationship("FinanceRecordModel", uselist=False)
    account_user = db.relationship("AccountUserModel", uselist=False, back_populates="money_type")

    def convert_to_dict(self):
        return {'id': self.money_id, 'name': self.money_name}


class AccountUserModel(db.Model):
    __tablename__ = 'account_user'

    user_id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, nullable=False)
    preferred_currency_id = db.Column(db.String(128), db.ForeignKey('money_type.money_id'), nullable=True)

    money_type = db.relationship('MoneyType', back_populates='account_user')
    finance_record = db.relationship('FinanceRecordModel', back_populates='account_user', lazy="dynamic")

    def convert_to_dict(self):
        return {'id': self.user_id, 'name': self.user_name, 'default_currency_id': self.preferred_currency_id}


class ExpenditureCategoryModel(db.Model):
    __tablename__ = 'expenditure_category'

    category_id = db.Column(db.String, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False)

    finance_record = db.relationship("FinanceRecordModel", back_populates="expenditure_category", lazy="dynamic")

    def convert_to_dict(self):
        return {'id': self.category_id, 'name': self.category_name}



class FinanceRecordModel(db.Model):
    __tablename__ = 'finance_record'

    record_id = db.Column(db.String, primary_key=True)
    amount_spent = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    time_stamp = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    currency_id = db.Column(db.String, nullable=False)

    def convert_to_dict(self):
        return {
            'id': self.record_id,
            'amount_spent': self.amount_spent,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'time_stamp': self.time_stamp,
            'currency_id': self.currency_id
        }

