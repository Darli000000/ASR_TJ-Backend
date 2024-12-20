from flask import Flask
from flask_restx import Api

# 初始化 Flask
def create_app():
    app = Flask(__name__)

    # 初始化 Flask-RESTx 的 API
    api = Api(app, version="1.0", title="API FunASR", description="A demo API with Flask-RESTx")

    # 导入并注册各个命名空间
    from app.routes.user_routes import user_ns
    from app.routes.product_routes import product_ns
    from app.routes.asr_routes import asr_ns

    api.add_namespace(user_ns, path="/users")  # 用户相关的 API
    api.add_namespace(product_ns, path="/products")  # 产品相关的 API (示例)
    api.add_namespace(asr_ns, path="/asr")  # 语音识别相关api

    return app
