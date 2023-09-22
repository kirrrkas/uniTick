from django.contrib import admin
from shop.models import *
from django.utils.html import mark_safe


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 1
    max_num = 7
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class ProductOptionInline(admin.StackedInline):
    model = ProductOption
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductPhotoInline, ProductOptionInline)
    list_display = ('id', 'club', 'name', 'price', 'availability')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'price', 'description', 'availability', 'club', 'categories')
    save_on_top = True
    filter_horizontal = ('categories',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    fields = ('name',)
    save_on_top = True


@admin.register(OptionValue)
class OptionValueAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    fields = ('option', 'value')
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug')
    save_on_top = True


class OrderDetailsInline(admin.StackedInline):
    model = OrderDetails

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderDetailsInline,)
    list_display = ('id', 'customer', 'status', 'time_create')
    list_display_links = ('id', 'customer')
    fields = ('customer', 'email', 'phone_number', 'status', 'shipping_address', 'cost_order')
    readonly_fields = ('customer', 'email', 'phone_number', 'shipping_address', 'cost_order')
    save_on_top = True

    def has_add_permission(self, request, obj=None):
        return False
