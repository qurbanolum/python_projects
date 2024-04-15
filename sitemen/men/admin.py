from django.contrib import admin, messages
from django.contrib.messages import WARNING
from django.utils.safestring import mark_safe

from men.models import Men, Category



class MarriedFilter(admin.SimpleListFilter):
    title = 'Marriage status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Married'),
            ('single',   'Single'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)

@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    fields = ['title', 'photo', 'post_photo', 'content', 'slug', 'cat', 'wife', 'tags']
    readonly_fields = ['post_photo']
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    actions = ['set_published', 'set_unpublished']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']

    @admin.display(description='Photo', ordering='content')
    def post_photo(self, men: Men):
        if men.photo:
            return mark_safe(f"<img src='{men.photo.url}' width=50>")
        else:
            return 'No photo'
    @admin.action(description='Publicate chosen posts')
    def set_published(self, request, query_set):
        count = query_set.update(is_published=Men.Status.PUBLISHED)
        self.message_user(request, f'Updated {count} posts')

    @admin.action(description='Unpublish chosen posts')
    def set_unpublished(self, request, query_set):
        count = query_set.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f'Unpubliced {count} posts', messages.WARNING)

@admin.register(Category)
class MenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
