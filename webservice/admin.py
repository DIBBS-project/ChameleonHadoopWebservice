from django.contrib import admin
from .models import User, Site, Cluster, Host, Software, Script, Event

admin.site.register(User)
admin.site.register(Site)
admin.site.register(Cluster)
admin.site.register(Host)
admin.site.register(Software)
admin.site.register(Script)
admin.site.register(Event)