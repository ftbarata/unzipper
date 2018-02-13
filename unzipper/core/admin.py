from django.contrib import admin
from .models import UsersForPath, Paths, PermissionsProfileConfig, RegisteredMailDomains

admin.site.register(UsersForPath)
admin.site.register(Paths)
admin.site.register(PermissionsProfileConfig)
admin.site.register(RegisteredMailDomains)