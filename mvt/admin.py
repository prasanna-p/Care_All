from django.contrib import admin
from mvt.models import CareTaker
from mvt.models import CareSeeker
from mvt.models import Request
from mvt.models import Review
from mvt.models import FundTransferRecord


# Register your models here.
# admin.site.register(post)
admin.site.register(CareTaker)
admin.site.register(CareSeeker)
admin.site.register(Request)
admin.site.register(Review)
admin.site.register(FundTransferRecord)