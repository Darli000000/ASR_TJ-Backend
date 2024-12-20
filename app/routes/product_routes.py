from flask_restx import Namespace, Resource, fields

# 定义命名空间
product_ns = Namespace("products", description="Product operations")

# 定义数据模型
product_model = product_ns.model("Product", {
    "id": fields.Integer(readOnly=True, description="Product ID"),
    "name": fields.String(required=True, description="Product name"),
    "price": fields.Float(required=True, description="Product price")
})

# 模拟产品数据库
products = []

# 获取所有产品
@product_ns.route("/")
class ProductList(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        """获取所有产品"""
        return products

    @product_ns.expect(product_model)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        """创建新产品"""
        new_product = product_ns.payload
        new_product["id"] = len(products) + 1
        products.append(new_product)
        return new_product, 201