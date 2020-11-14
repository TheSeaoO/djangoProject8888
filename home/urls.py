#-*-coding:utf-8 -*-

from django.urls import path, include, re_path
from .views import *
from django.contrib import admin


urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),

    # 个人中心
    path('user_info/', user_info, name="user_info"),
    path('change_userinfo/', change_userinfo, name="change_userinfo"),
    path('change_password/', change_password, name="change_password"),
    path('forget_password/', forget_password, name="forget_password"),
    path('send_code/', send_code, name="send_code"),
    path('reg_send_code/', reg_send_code, name="reg_send_code"),

    # 漂流瓶信息
    path('my_bottle_message/', my_bottle_message, name="my_bottle_message"),
    path('add_bottle/', add_bottle, name="add_bottle"),
    path('bottle_message/', bottle_message, name="bottle_message"),
    path('bottle_detail/<int:id>', bottle_detail, name="bottle_detail"),
    path('pick_message/', pick_message, name="pick_message"),
    path('pick_one/', pick_one, name="pick_one"),
    path('visit_page/<int:id>', visit_page, name="visit_page"),
    path('site_detail/<int:id>', site_detail, name="site_detail"),
    path('throw_sea/<int:id>', throw_sea, name="throw_sea"),
    path('reply_bottle/<int:id>', reply_bottle, name="reply_bottle"),
    # 投放
    path('launch/<int:id>', launch, name="launch"),
    path('delete_bottle/<int:id>', delete_bottle, name="delete_bottle"),
]

app_name = "home"


from .add_data import *
# 数据添加接口
urlpatterns += [
    path('add_bottle_type/', add_bottle_type, name="add_bottle_type"),
]