
from base import BtwBaseHandler
from models.user import UserModel

class UserManageHandler(BtwBaseHandler):

    def get(self, merchant_id):
        '''
        users = UserModel.get_users_by_merchant_id(merchant_id)
        '''
        return self.render("userManage.html", users=None)
