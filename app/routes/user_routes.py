from flask_restx import Namespace, Resource, fields

# 定义命名空间
user_ns = Namespace("users", description="User operations")

# 定义数据模型
user_model = user_ns.model("User", {
"id": fields.Integer(readOnly=True, description="User ID"),
"username": fields.String(required=True, description="User name"),
"email": fields.String(required=True, description="User email")
})

# 模拟数据库
users = []

# 获取所有用户
@user_ns.route("/")
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """获取所有用户"""
        return users

    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """创建新用户"""
        new_user = user_ns.payload
        new_user["id"] = len(users) + 1
        users.append(new_user)
        return new_user, 201


# 获取单个用户
@user_ns.route("/<int:id>")
@user_ns.param("id", "User ID")
class User(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, id):
        """获取单个用户"""
        user = next((u for u in users if u["id"] == id), None)
        if not user:
            user_ns.abort(404, "User not found")
        return user

    def delete(self, id):
        """删除用户"""
        global users
        users = [u for u in users if u["id"] != id]
        return {"message": "User deleted"}, 200
