from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from shop.models import *

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomColorAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'color_hex', 'slug')
    search_fields = ('color_name', 'color_hex')
    readonly_fields = ('slug',)
    ordering = ('color_name',)


class CustomCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'color', 'slug', 'image')
    search_fields = ('product_name', 'category__category_name',
                     'color__color_name', 'color__color_hex')
    readonly_fields = ('slug',)
    ordering = ('product_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'size', 'price', 'stock', 'sold')
    search_fields = ('product', 'size', 'price', 'stock', 'sold')
    ordering = ('product',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_product_name(self, obj):
        return '{} - {}'.format(str(obj.product.product_name), str(obj.product.color.color_name))
    get_product_name.short_description = 'product'


class CustomOrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'added_date',
                    'quantity', 'ordered')
    search_fields = ('user', 'item', 'added_date', 'quantity')
    ordering = ('user',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'city',
                    'state', 'zipcode', 'country')
    search_fields = ('user', 'order', 'address', 'city',
                     'state', 'zipcode', 'country')
    ordering = ('user',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(Color, CustomColorAdmin)
admin.site.register(Size)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(Item, CustomItemAdmin)
admin.site.register(OrderItem, CustomOrderItemAdmin)
admin.site.register(Order)
admin.site.register(ShippingAddress, CustomShippingAddressAdmin)
