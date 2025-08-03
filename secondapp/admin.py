from django.contrib import admin
import secondapp.models
# Register your models here.

admin.site.site_header = "My Website | Second Project"

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'roll_num', 'fee', 'is_registered']
    search_fields = ['name', 'email', 'roll_num']
    list_filter = ['is_registered','name','gender']
    list_editable = ['fee', 'is_registered']

class Contact_UsAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'contact_number', 'subject', 'added_on']
    search_fields = ['name', 'contact_number', 'subject']
    list_filter = ['added_on']
    list_editable = ['subject']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name', 'cover_pic', 'description', 'added_on']
    search_fields = ['cat_name', 'description']
    list_filter = ['added_on']
    list_editable = ['description']    

admin.site.register(secondapp.models.Student, StudentAdmin)
admin.site.register(secondapp.models.Contact_Us, Contact_UsAdmin)
admin.site.register(secondapp.models.Category, CategoryAdmin)
admin.site.register(secondapp.models.register_table)
admin.site.register(secondapp.models.add_product)
admin.site.register(secondapp.models.cart)
admin.site.register(secondapp.models.Order)