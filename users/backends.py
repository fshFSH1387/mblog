# from django.contrib.auth.handlers.modwsgi import check_password
# from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import check_password

from users.models import User

class EmailBackend(object):
    def authenticate(self, request, **credentials):
        # 根据邮箱找用户，找到了才能判断密码
        # 取出email
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            # 检验
            if user.check_password(credentials['password']):
                return user
        pass

    # 必须要定义
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
