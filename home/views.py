from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.shortcuts import HttpResponseRedirect, HttpResponse
from home.forms import UserForm
from djangoProject4.common import setPassword, loginValid, send_email, set_page
from string import ascii_letters, digits
from django.db.models import Q, F
from django.utils import timezone
import random


@loginValid
def index(request):
    user_id = request.session.get("user_id")
    # 已投放
    bottle_number = Bottle.objects.filter(user_id=user_id, status=1).count()
    # 已捞起
    save_number = Bottle.objects.filter(pick_user_id=user_id, status=2).count()
    # 未投放
    not_released = Bottle.objects.filter(user_id=user_id, status=0)[:6]
    # 未回复
    not_comment = Bottle.objects.filter(pick_user_id=user_id, status=2, reply_status=0)[:6]
    return render(request, "common/index.html",
                  {"bottle_number": bottle_number, "save_number": save_number, "not_released": not_released,
                   "not_comment": not_comment})


# 注册页面
def register(request):
    error_msg = ""
    if request.method == "POST":
        userform = UserForm(request.POST)  # 将请求的数据加入表单进行校验
        if userform.is_valid():
            data = request.POST
            username = userform.cleaned_data.get("username")
            password = userform.cleaned_data.get("password")
            password_confirm = data.get("password_confirm")
            code = data.get("code")
            email = data.get("email")
            if password != password_confirm:
                error_msg = "两次密码不一致"
                return render(request, "common/register.html", {"errors": error_msg})
                # 数据库保存用户注册信息
            code1 = request.session.get("code")
            email1 = request.session.get("email")
            print(code1, email1, code, email)
            if code != code1 or email != email1:
                error_msg = "验证码与邮箱不符"
                return render(request, "common/register.html", {"errors": error_msg})
            try:
                user = User()
                user.username = username
                user.password = setPassword(setPassword(password))
                user.email = email
                user.save()
                return HttpResponseRedirect("/login/")
            except:
                error_msg = "邮箱或者用户名重复！"
        else:
            error_msg = userform.errors
    return render(request, "common/register.html", {"errors": error_msg})


# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = User.objects.filter(username=username, password=setPassword(setPassword(password)))
        if u.exists():
            response = HttpResponseRedirect("/")
            response.set_cookie("username", username)
            request.session["username"] = username
            request.session["user_id"] = u[0].id
            request.session["image"] = u[0].image.path
            return response
        else:
            error_msg = '用户名或密码错误'
            return render(request, "common/login.html", {'error_msg': error_msg})
    return render(request, "common/login.html")


# 退出
def logout(request):
    response = HttpResponseRedirect("/login/")
    try:
        response.delete_cookie("username")
        del request.session["username"]
        del request.session["user_id"]
        del request.session["image"]
    except Exception as e:
        pass
    return response


# 个人信息
@loginValid
def user_info(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)
    if user.exists():
        user = user[0]
        return render(request, "common/user_info.html", locals())
    else:
        return render(request, "common/pages-404.html")


# 修改个人信息
@loginValid
def change_userinfo(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)

    if not user.exists():
        return render(request, "common/pages-404.html")

    if request.method == "POST":
        data = request.POST
        nick_name = data.get("nick_name")
        gender = data.get("gender")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        image = request.FILES.get("image")
        print(image)
        user.update(
            nick_name=nick_name if nick_name else F("nick_name"),
            gender=gender if gender else F("gender"),
            phone=phone if phone else F("phone"),
            email=email if email else F("email"),
            address=address if address else F("address")
        )
        if image:
            user = user[0]
            user.image = image
            user.save()
        return redirect("home:user_info")

    return render(request, "common/change_userinfo.html", {"user": user[0]})


# 修改密码
@loginValid
def change_password(request):
    user_id = request.session.get("user_id")
    error = ""
    if request.method == "POST":
        data = request.POST
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        password_sure = data.get("password_sure")
        user = User.objects.filter(id=user_id, password=setPassword(setPassword(old_password)))
        if new_password == password_sure and user.exists():
            user.update(password=setPassword(setPassword(new_password)))
            return redirect("home:logout")
        else:
            error = "原密码错误或两次密码不一致！"
    return render(request, "common/change_password.html", {"error": error})


# 忘记密码
def forget_password(request):
    error = ""
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        code = data.get("code")
        password = data.get("password")
        alternative_code = request.session.get("code")
        alternative_email1 = request.session.get("email")
        if email == alternative_email1 and code == alternative_code:
            User.objects.filter(email=email).update(password=setPassword(setPassword(password)))
            return redirect("home:login")
        error = "邮箱或验证码不正确，请确认！"
    return render(request, "common/forget_password.html", {"error": error})


# ajax 发送验证码
def send_code(request):
    response = {"status": 0, "data": "邮箱有误，请确认邮箱"}
    email = request.GET.get("email")
    u = User.objects.filter(email=email)
    if u.exists():
        alternate_string = ascii_letters + digits
        str1 = ""
        for i in range(6):
            str1 += random.choice(alternate_string)
        #print(str1)
        result = send_email(str1, email)
        if result:
            response["status"] = 1
            response["data"] = "验证码已发送，请查收"
            request.session["code"] = str1
            request.session["email"] = email
    #print(response, 11111111)
    return JsonResponse(response)


# 未投放
def my_bottle_message(request):
    user_id = request.session.get("user_id")
    bottle_list = Bottle.objects.filter(user_id=user_id, status="0")
    page = request.GET.get("page", 0)
    data, page_list = set_page(bottle_list, 20, page)
    return render(request, "common/my_bottle_message.html", {"data": data, "page_list": page_list})


# 新增漂流瓶
@loginValid
def add_bottle(request):
    if request.method == "GET":
        return render(request, "common/add_bootle.html")
    else:
        data = request.POST
        now_date = timezone.now().strftime("%Y-%m-%d")
        bottle_title = data.get("tittle")
        content = data.get("content")
        status = data.get("status")
        user_id = request.session.get("user_id")
        count = Bottle.objects.filter(user_id=user_id, add_date=now_date).count()
        if count >= 10:
            return HttpResponse("今日漂流瓶数量已达上限")
        Bottle.objects.create(bottle_title=bottle_title, bottle_content=content, status=status, user_id=user_id)
        return redirect("home:my_bottle_message")


# 投放
def launch(request, id):
    date = timezone.now()
    user_id = request.session.get("user_id")
    bottle = Bottle.objects.filter(user_id=user_id, id=id)
    bottle.update(status="1", launch_time=date)
    return redirect("home:bottle_message")


# 删除
def delete_bottle(request, id):
    user_id = request.session.get("user_id")
    Bottle.objects.filter(user_id=user_id, id=id).delete()
    return redirect("home:my_bottle_message")


# 注册时发送验证码
def reg_send_code(request):
    response = {"status": 0, "data": "邮箱有误，请确认邮箱"}
    email = request.GET.get("email")
    alternate_string = ascii_letters + digits
    str1 = ""
    for i in range(6):
        str1 += random.choice(alternate_string)
    result = send_email(str1, email)
    if result:
        response["status"] = 1
        response["data"] = "验证码已发送，请查收"
        request.session["code"] = str1
        request.session["email"] = email
    return JsonResponse(response)


# 已投放信息
@loginValid
def bottle_message(request):
    user_id = request.session.get("user_id")
    bottle_title = request.GET.get("bottle_title", "")
    bottle_content = request.GET.get("bottle_content", "")
    if bottle_title or bottle_content:
        bottle_list = Bottle.objects.filter(
            Q(bottle_title__icontains=bottle_title) or Q(bottle_content__icontains=bottle_content), user_id=user_id,
            status="1").order_by("id")
    else:
        bottle_list = Bottle.objects.filter(user_id=user_id, status="1")
    page = request.GET.get("page", 0)
    data, page_list = set_page(bottle_list, 20, page)
    return render(request, "common/bottle_message.html",
                  {"data": data, "page_list": page_list, "bottle_title": bottle_title,
                   "bottle_content": bottle_content})


# 漂流瓶详情
@loginValid
def bottle_detail(request, id):
    bottle = Bottle.objects.filter(id=id)
    if not bottle.exists():
        return render(request, "common/pages-404.html")
    print(bottle)
    return render(request, "common/bottle_detail.html", {"bottle": bottle[0]})


# 已捞起记录
@loginValid
def pick_message(request):
    user_id = request.session.get("user_id")
    pick_list = Bottle.objects.filter(pick_user_id=user_id).order_by("-pick_up_time")
    page = request.GET.get("page", 0)
    data, page_list = set_page(pick_list, 20, page)
    return render(request, "common/pick_message.html", {"data": data, "page_list": page_list})


# 捞一个
@loginValid
def pick_one(request):
    if Bottle.objects.filter(status=1):
        now_time = timezone.now()
        user_id = request.session.get("user_id")
        now_date = timezone.now().strftime("%Y-%m-%d")
        count = PickRecords.objects.filter(user_id=user_id, add_date=now_date).count()
        if count >= 10:
            return HttpResponse("今日捞起数量已达上限")
        bottle = Bottle.objects.filter(status="1", pick_user__isnull=True)
        bottle = random.choice(bottle)
        bottle.pick_up_time = now_time
        bottle.pick_user_id = user_id
        bottle.status = "2"
        bottle.save()
        PickRecords.objects.create(user_id=user_id, bottle_id=bottle.id)
    else:
        error_msg = '暂无漂流瓶'
        return render(request, "common/pick_message.html", {'error_msg': error_msg})
    return redirect("home:pick_message")


def throw_sea(request, id):
    bottle = Bottle.objects.filter(id=id).update(pick_up_time=None, pick_user_id=None, status="1")
    return redirect("home:pick_message")


@loginValid
def reply_bottle(request, id):
    if request.method == "GET":
        bottle = Bottle.objects.filter(id=id).first()
        edit = request.GET.get("edit", False)
        if edit:
            return render(request, "common/reply_bootle.html", {"bottle": bottle, "edit": edit})
        comment_list = Comment.objects.filter(bottle_id=id)
        return render(request, "common/reply_bootle.html",
                      {"bottle": bottle, "comment_list": comment_list, "edit": edit})
    else:
        user_id = request.session.get("user_id")
        data = request.POST
        comment = data.get("comment")
        bottle_id = data.get("bottle_id")
        Bottle.objects.filter(id=bottle_id).update(reply_status=1, delete=1)
        Comment.objects.create(
            comment_user_id=user_id,
            comment=comment,
            bottle_id=bottle_id
        )
        return redirect("home:pick_message")


# 站点详情
@loginValid
def site_detail(request, id):
    return render(request, "common/site_detail.html")


@loginValid
def visit_page(request, id):
    user = User.objects.filter(id=id)
    if user.exists():
        user = user[0]
        return render(request, "common/user_info.html", locals())
    else:
        return render(request, "common/pages-404.html")
