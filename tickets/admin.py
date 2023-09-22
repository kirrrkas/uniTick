from django.contrib import admin
from tickets.models import *
from django.utils.html import mark_safe


class MatchClubInline(admin.StackedInline):
    model = MatchClub

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    inlines = (MatchClubInline,)
    list_display = ('id', 'name', 'city', 'get_html_logo')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'city')
    list_filter = ('city', )
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'city', 'logo', 'get_html_logo', 'stadiums')
    readonly_fields = ('get_html_logo',)
    save_on_top = True
    filter_horizontal = ('stadiums',)

    def get_html_logo(self, object):
        if object.logo:
            return mark_safe(f"<img src='{object.logo.url}' width=50>")

    get_html_logo.short_description = "Миниатюра"


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
