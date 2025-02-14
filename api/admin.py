from django.contrib import admin

from api.models import User,OTM,Student,Sponsor,Sponsorship

admin.site.register(User)
admin.site.register(OTM)
admin.site.register(Student)
admin.site.register(Sponsor)
admin.site.register(Sponsorship)
