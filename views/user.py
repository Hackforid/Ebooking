
from base import BtwBaseHandler
from models.user import UserModel
from tornado.escape import json_encode
from tools import auth

class UserManageHandler(BtwBaseHandler):

    def get(self, merchant_id):
        users = UserModel.get_users_by_merchant_id(self.db, merchant_id)
        return self.render("userManage.html", users=json_encode([user.todict() for user in users]))

    def put(self, user_info):



