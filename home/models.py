from django.db import models


# 用户数据表
class User(models.Model):
    class Meta:
        verbose_name = "普通用户"
        verbose_name_plural = "普通用户"

    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")  # 不可以重复
    password = models.CharField(max_length=32, verbose_name="密码")
    nick_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="昵称")
    gender = models.BooleanField(default=1, verbose_name="性别")
    phone = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name="手机号")
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="邮箱")
    address = models.TextField(blank=True, null=True, verbose_name="地址")
    image = models.ImageField(upload_to='upload/user', default='upload/user/!happy-face.png', verbose_name="用户头像")

    def __str__(self):
        return self.username


# 漂流瓶
class Bottle(models.Model):
    class Meta:
        verbose_name = "漂流瓶"
        verbose_name_plural = "漂流瓶"

    STATUS = (
        (0, '未投放'),
        (1, '已投放'),
        (2, '已捞起'),
        (3, '已回复'),
    )
    bottle_title = models.CharField(verbose_name="漂流瓶名字", max_length=30)
    bottle_content = models.CharField(verbose_name="漂流瓶内容", max_length=100)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    add_date = models.DateField(verbose_name="创建日期", auto_now=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=1, verbose_name="发送者",related_name="send_user")
    status = models.CharField(choices=STATUS, max_length=1, verbose_name="状态")
    delete = models.BooleanField(default=0, verbose_name="是否可以删除")
    pick_user = models.ForeignKey("User",on_delete=models.SET_NULL,null=True, verbose_name="捞起人",related_name="pick_user")
    launch_time = models.DateTimeField(verbose_name="投放时间",null=True)
    pick_up_time = models.DateTimeField(verbose_name="捞起时间",null=True)
    reply_status = models.BooleanField(default=0,verbose_name="是否回复")
    def __str__(self):
        return self.bottle_title


#
class Comment(models.Model):
    class Meta:
        verbose_name = "漂流瓶"
        verbose_name_plural = "漂流瓶"

    comment = models.CharField(verbose_name="回复内容", max_length=100)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    comment_user = models.ForeignKey("User", on_delete=models.CASCADE, default=1, verbose_name="评论人")
    bottle = models.ForeignKey("Bottle", on_delete=models.CASCADE, default=1, verbose_name="漂流瓶")

    def __str__(self):
        return self.comment


#
class PickRecords(models.Model):
    class Meta:
        verbose_name = "捞起记录"
        verbose_name_plural = "捞起记录"

    bottle = models.ForeignKey("Bottle", on_delete=models.CASCADE, default=1, verbose_name="漂流瓶")
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=1, verbose_name="捞起人")
    add_date = models.DateField(verbose_name="捞起日期", auto_now=True)

