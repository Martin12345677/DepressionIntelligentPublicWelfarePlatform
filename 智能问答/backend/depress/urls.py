from django.urls import path

from . import views
from .api import api, getReply

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('change_mode', views.change_mode, name='change_mode'),
    path('signup', views.signup, name='signup'),
    path('getReply', getReply.reply, name='getReply'),
    path('getHistory', api.get_history, name='getHistory'),
    path('znwd', views.znwd, name='znwd'),
    path('aqtc', views.aqtc, name='aqtc'),
    path('xgzl', views.xgzl, name='xgzl'),
    # path('add', api.add_test, name='add'),
    path('test', views.test, name='test'),
    path('xlpg', views.xlpg, name='xlpg'),
    path('test_result', views.test_result),
    path('sendVerify', api.send_verify)
]
