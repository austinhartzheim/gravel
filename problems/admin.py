from django.contrib import admin
from problems import models


admin.site.register(models.Problem)
admin.site.register(models.ProblemTag)
admin.site.register(models.Reply)
