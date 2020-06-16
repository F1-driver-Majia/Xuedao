from django.db import models
class Wx_user(models.Model):
    openid = models.CharField(max_length=128,primary_key=True)
    name = models.CharField(max_length=30,default='新用户')
    sexy = models.IntegerField(default=1)
    intro = models.CharField(max_length=400,blank=True)

class Lessons(models.Model):
    name = models.CharField(max_length=30)
    intro = models.CharField(max_length=500)

class Subjects(models.Model):
    name = models.CharField(max_length=30)
    intro = models.CharField(max_length=500)
    lessons = models.ManyToManyField(Lessons,related_name='lessons')


class Recommends(models.Model):
    user_name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=128)
    content = models.CharField(max_length=2000)
    title = models.CharField(max_length=30)
    lesson = models.ForeignKey(Lessons,on_delete=models.CASCADE)
    cover1 = models.ImageField(upload_to='img',null=True,blank=True)
    cover2 = models.ImageField(upload_to='img',null=True,blank=True)
    cover3 = models.ImageField(upload_to='img',null=True,blank=True)
    time = models.DateField(auto_now=True)
    col_count = models.IntegerField(default=0,db_index=True)



class Comments(models.Model):
    user_name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=128)
    content = models.CharField(max_length=200)
    recommend = models.ForeignKey(Recommends,related_name='comments',on_delete=models.CASCADE)
    #约束名称在序列化时很重要
class Colletions(models.Model):
    user_id = models.CharField(max_length=128)
    recommend = models.ForeignKey(Recommends,related_name='colletions',on_delete=models.CASCADE)
    # 约束名称在序列化时很重要