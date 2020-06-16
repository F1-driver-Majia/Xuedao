from rest_framework import serializers

from myblog.models import Lessons, Subjects, Comments, Recommends


class Wx_userSerializer(serializers.Serializer):
    openid = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=30)
    intro = serializers.CharField(max_length=400)
    sexy = serializers.IntegerField()

class Less_Srializer(serializers.ModelSerializer):
    #lessons的序列化
    class Meta:
        model = Lessons
        fields = '__all__'

class Sub_Serializer(serializers.ModelSerializer):
    #学科和课程的序列化
    lessons = Less_Srializer(many=True)
    #引入lessons的序列化器
    #related_name约束名要和字段名相同
    class Meta:
        model = Subjects
        fields = ('id','name','intro','lessons')

class Com_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('user_name','user_id','content')


class Rec_Serializer(serializers.ModelSerializer):
    #推荐的序列化
    class Meta:
        model = Recommends
        fields = ('__all__')