from django.contrib import admin
from .models import User, Test, History, Record, LabelRecord, Label, Problem, Answers

# Register your models here.

admin.site.register(User)
admin.site.register(Test)
admin.site.register(History)
admin.site.register(Record)
admin.site.register(LabelRecord)
admin.site.register(Label)
admin.site.register(Problem)
admin.site.register(Answers)
