from django.contrib import admin
from .models import Recruiter, User_Recruiter
from import_export.admin import ImportExportModelAdmin # type: ignore

# Register your models here.



class RecruiterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class User_RecruiterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Recruiter, RecruiterAdmin)
admin.site.register(User_Recruiter, User_RecruiterAdmin)
