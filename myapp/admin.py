from django.contrib import admin
from .models import   Project , Project_Milestone, Manager , Status , Project_Type  , Permission , Roles , UserAndRoles , Staff  


admin.site.register(Project)
admin.site.register(Project_Milestone)
admin.site.register(Manager)
admin.site.register(Status)
admin.site.register(Project_Type)
admin.site.register(Roles)
admin.site.register(Permission)
admin.site.register(UserAndRoles)
admin.site.register(Staff)





