from django.contrib import admin
from .models import Snippet, Comment, Tag
from django.db.models import Count


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('name', 'lang', 'user', 'num_comments')
    list_filter = ('lang', 'public')
    search_fields = ['name', 'code']

    # Метод для получения queryset с аннотированным полем
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Аннотируем каждую запись количеством комментариев
        queryset = queryset.annotate(
            num_comments=Count('comments', distinct=True)
        )
        return queryset

    # Добавление пользовательского поля
    def num_comments(self, obj):
        return obj.num_comments

    # Определение заголовка для пользовательского поля
    num_comments.short_description = 'Кол-во комментариев'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'snippet', 'creation_date')
    list_filter = ('creation_date', 'author')
    search_fields = ['author__username', 'snippet__name', 'text']


class TagAdmin(admin.ModelAdmin):
    #list_display = ('name',)
    search_fields = ['name']




# Register your models here.
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)