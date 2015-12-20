from django.contrib import admin
import core.models as coremodels

# Register your models here.

admin.site.register(coremodels.Theme)
admin.site.register(coremodels.Item)
admin.site.register(coremodels.Entry)
admin.site.register(coremodels.UserProfile)
