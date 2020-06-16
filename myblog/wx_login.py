from web1 import settings
import requests

# 调用微信code2Session接口,换取用户唯一标识 OpenID 和 会话密钥 session_key
def login(code):
    response = requests.get(settings.code2Session.format(settings.AppId,settings.AppSecret,code))
    data = response.json()
    if data.get("openid"):
        return data
    else:
        return False