from django.contrib import admin
from .models import *


admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Card)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Order)