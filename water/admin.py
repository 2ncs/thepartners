from django.contrib import admin

# Register your models here.

from .models import *
# Register your models here.
class PricesInline(admin.StackedInline):
    model = Number_of_travelers()

class MyAppUserAdmin(admin.ModelAdmin):
    inlines = [
        PricesInline,
    ]

admin.site.register(MyAppUser)
admin.site.register(Clients)
admin.site.register(Number_of_travelers)
admin.site.register(sales)
admin.site.register(customers_served)


