from django.contrib import admin
from dashboard.models import Homework, Notes,stNotes, Helppost ,notice
from dashboard.models import Todo

admin.site.register(stNotes)
# Register your models here.
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
admin.site.register(Helppost)
admin.site.register(notice)
