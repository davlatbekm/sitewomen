from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category, UploadFiles
# Register your models here.
class MarriedFilter(admin.SimpleListFilter):
    title = 'Status Women'
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        return [
            ('married', 'Married'),
            ('single', 'Single'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'photo', 'post_photo','cat', 'husband', 'tags', 'author']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'post_photo', "time_created", 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ['time_created', 'title']
    list_editable = ('is_published', )
    list_per_page = 10
    actions = ['set_published',  'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = (MarriedFilter, "cat__name", 'is_published')
    filter_vertical = ['tags']
    save_on_top = True


    @admin.display(description='Current Photo', ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        else:
            return "Without photo"

    @admin.action(description='Publish selected data')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Published {count} entries.", messages.SUCCESS)


    @admin.action(description='Draft selected data')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Drafted {count} entries.", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(UploadFiles)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
