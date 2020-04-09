from django.contrib import admin
from todolist_app.models import Priority, Todo


class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


admin.site.register(Priority, PriorityAdmin)
admin.site.register(Todo)
