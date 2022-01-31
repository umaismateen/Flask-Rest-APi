from product_api import ma
from product_api.models import Product, User


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
    product = ma.auto_field()
    product_id = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    user_id = ma.auto_field()
    username = ma.auto_field()


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
