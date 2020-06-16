import hashlib
import time
import  datetime
from myblog.models import Wx_user, Recommends, Lessons
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from myblog import wx_login
from myblog import models
from myblog import seria
#记得在setting中也添加







class LoginView(APIView):
#登录接口
    def post(self,request):

        code = request.data['code']
        data = wx_login.login(code)
        if data:
            # 将openid 和 session_key拼接
            val = data['openid'] + "&" + data["session_key"]
            key = data["openid"] + str(int(time.time()))
            # 将 key 加密
            md5 = hashlib.md5()
            md5.update(key.encode("utf-8"))
            key = md5.hexdigest()
            # 保存到redis内存库,因为小程序端后续需要认证的操作会需要频繁校验
            cache.set(key, val,60*3600)
            val = cache.get(key)

            print(key)
            print(val)
            #用户不存在则创建用户
            has_user = Wx_user.objects.filter(openid=data['openid']).first()
            if not has_user:
                Wx_user.objects.create(openid=data['openid'])
                return Response(data={'Loginid':key,'msg':'已创建用户'},status=200)
            else:
                return Response(data={'Loginid':key,'msg':'登录成功'},status=200)
        else:
            return Response({"code": 401, "msg": "缺少参数"})

    def get(self, request):
        return



class ProfileView(APIView):
    #资料页面
    def  get(self, request):
        key = request.query_params.get('Loginid')

        val = cache.get(key)
        #从缓存中获取session

        userid = val.split('&')[0]

        user = Wx_user.objects.filter(openid=userid).first()
        res = seria.Wx_userSerializer(instance=user)
        #取出数据并序列化

        return Response(status=200,data=res.data)

    def post(self, request):
        print(request.data)
        res=request.data


        Loginid = res.get('Loginid')
        #取出session_key
        val = cache.get(Loginid)
        userid = val.split('&')[0]
        #openid


        Wx_user.objects.filter(openid=userid).update(name=res.get('name'),sexy=res.get('sexy'),intro=res.get('intro'))


        return Response(status=200)

class IniView(APIView):
    #程序初始化时获取学科和课程
    def get(self,request):
        sub = models.Subjects.objects.all()

        data = seria.Sub_Serializer(instance=sub,many=True).data


        return Response(data=data,status=200)

class UploadView(APIView):
    #推荐上传接口
    #用post发送图片，get发送文本

    def get(self,request):
        key = request.query_params.get('Loginid')

        val = cache.get(key)
        # 从缓存中获取session


        if not val:
            return Response({'msg': '用户未登录'}, status=400)



        userid = val.split('&')[0]
        username = models.Wx_user.objects.filter(openid=userid).first().name
        content = request.query_params.get('content')
        title = request.query_params.get('title')
        les_id = request.query_params.get('les_id')
        less = Lessons.objects.get(id=les_id)
        time = datetime.datetime.now().date()


        rec = Recommends.objects.create(user_id=userid,user_name=username,content=content,title=title,lesson=less)

        #用cache暂时保存recommend的id
        cache.set(userid,rec.id,20)
        #目前该推荐应上传的图片序号
        cache.set(rec.id,1,10)

        return  Response({'msg' : '提交成功'},status=200)

    def post(self,request):
        key = request.data.get('Loginid')
        val = cache.get(key)
        # 从缓存中获取session
        userid = val.split('&')[0]

        img = request.FILES.get('file')
        print(img)
        #获取recid
        recid = cache.get(userid)

        #获取对应的封面序号
        i = cache.get(recid)
        cache.set(recid,i+1,10)

        rec = Recommends.objects.get(id=recid)


        exec('rec.cover{}=img'.format(i))

        rec.save()

        print(rec.cover1)

        return Response(status=200)



class ListView(APIView):
    def get(self,request):
        type = request.query_params.get('type')
        if type == '0':
            #打开学科的推荐列表
            lesson_id = request.query_params.get('lesson_id')

            recommends = Recommends.objects.filter(lesson=Lessons.objects.get(id=lesson_id)).order_by('-col_count')
            #查找推荐列表，并按收藏数降序
            data = seria.Rec_Serializer(instance=recommends,many = True)

            return Response(data=data.data, status=200)

        if type == '1':
            #打开自己的推荐
            key = request.query_params.get('Loginid')

            val = cache.get(key)
            # 从缓存中获取session

            userid = val.split('&')[0]

            recommends = Recommends.objects.filter(user_id=userid).order_by('-col_count')
            data = seria.Rec_Serializer(instance=recommends,many=True)


            return Response(data=data.data, status=200)

        if type == '2':
            #打开自己的收藏
            key = request.query_params.get('Loginid')

            val = cache.get(key)
            # 从缓存中获取session
            userid = val.split('&')[0]

            collections = models.Colletions.objects.filter(user_id=userid).select_related('recommend')
            recommends = set()
            for item in collections:
                recommends.add(item.recommend)

            #查找对应的收藏并查出收藏对应的推荐
            data = seria.Rec_Serializer(instance=recommends, many=True)

            return Response(data=data.data, status=200)


        return Response(status=400)

class DetailView(APIView):
    #推荐详情页的接口
    def get(self,request):
        rec_id = request.query_params.get('rec_id')
        Loginid = request.query_params.get('Loginid')

        if(Loginid==None):
            #没有登陆状态
            rec = models.Recommends.objects.get(id=rec_id)
            data = seria.Rec_Serializer(instance=rec)

            return Response({'isCollected':False,'data':data.data}, status=200)

        else:
            key = request.query_params.get('Loginid')

            val = cache.get(key)
            # 从缓存中获取session

            userid = val.split('&')[0]

            collect = models.Colletions.objects.filter(user_id=userid,recommend_id=rec_id)
            isCollected = False
            if (len(collect) != 0):
                isCollected = True

            rec = models.Recommends.objects.get(id=rec_id)
            data = seria.Rec_Serializer(instance=rec)




            return Response({'isCollected': isCollected, 'data': data.data}, status=200)

    def post(self,request):

        return Response()

class CommentView(APIView):

    def get(self,request):
        rec_id = request.query_params.get('rec_id')
        rec = models.Recommends.objects.get(id=rec_id)
        comments = models.Comments.objects.filter(recommend=rec)
        data = seria.Com_Serializer(instance=comments,many=True)

        return Response(data.data,status=200)

    def post(self,request):
        rec_id = request.data.get('rec_id')
        content = request.data.get('content')

        key = request.data.get('Loginid')
        val = cache.get(key)
        # 从缓存中获取session
        userid = val.split('&')[0]
        username = models.Wx_user.objects.get(openid=userid).name

        rec = models.Recommends.objects.get(id=rec_id)

        models.Comments.objects.create(recommend=rec,user_id=userid,user_name=username,content=content)

        return Response(status=200)

class CollectView(APIView):
    def get(self,request):
        rec_id = request.query_params.get('rec_id')

        key = request.query_params.get('Loginid')
        val = cache.get(key)
        # 从缓存中获取session
        userid = val.split('&')[0]

        rec = models.Recommends.objects.get(id=rec_id)

        col = models.Colletions.objects.filter(user_id=userid,recommend=rec)

        if(len(col)!=0):
            col.delete()
            rec.col_count = rec.col_count - 1
            rec.save()
            #增加收藏数
        else:
            models.Colletions.objects.create(user_id=userid, recommend=rec)
            rec.col_count = rec.col_count + 1
            rec.save()
            #减少收藏数

        return  Response(status=200)