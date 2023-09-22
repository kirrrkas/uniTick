from django.contrib import admin
from info.models import Article, ClubInfo, TournamentInfo
from django.utils.html import mark_safe


@admin.register(Article)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('clubs', 'tournaments', 'is_published', )
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'content', 'image', 'get_html_image', 'is_published', 'clubs', 'tournaments')
    filter_horizontal = ('clubs', 'tournaments')
    readonly_fields = ('get_html_image',)
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=250>")

    get_html_image.short_description = "Миниатюра"


@admin.register(ClubInfo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'tickets_key',)
    list_display_links = ('id', 'tickets_key')
    search_fields = ('description',)
    list_filter = ('tickets_key',)
    fields = ('tickets_key', 'description',)
    save_on_top = True


@admin.register(TournamentInfo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'tickets_key',)
    list_display_links = ('id', 'tickets_key')
    search_fields = ('description',)
    list_filter = ('tickets_key',)
    fields = ('tickets_key', 'description',)
    save_on_top = True
