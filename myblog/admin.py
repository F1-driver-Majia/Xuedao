from django.contrib import admin
from myblog.models import Wx_user
from myblog import models
#è½½å…¥Model
admin.site.register(Wx_user)
admin.site.register(models.Recommends)
admin.site.register(models.Lessons)
admin.site.register(models.Subjects)
admin.site.register(models.Colletions)
admin.site.register(models.Comments)

#使表在admin中可见
