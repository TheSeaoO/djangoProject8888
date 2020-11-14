#-*-coding:utf-8 -*-

from django.http import HttpResponse
from .models import *


# 随机插入漂流瓶
def add_bottle_type(request):
    user_list = User.objects.all()
    for i in range(2,60):
        bottle_title = "漂流瓶"+str(i)
        content = "漂流瓶内容"+str(i)
        for user in user_list:
            Bottle.objects.create(
                bottle_title=bottle_title,
                bottle_content=content,
                status="1",
                user_id=user.id
            )
    return HttpResponse("漂流瓶添加成功")

