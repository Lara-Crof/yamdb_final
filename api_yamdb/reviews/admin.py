from django.contrib import admin

from .models import Categories, Comment, Genres, Review, Title


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'slug',
                    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'slug',
                    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'year',
                    'description',
                    'category',
                    )
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text',
                    'author',
                    'score',
                    'pub_date',
                    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',
                    'author',
                    'review',
                    'review',
                    'pub_date',
                    )
    search_fields = ('text',)
    list_filter = ('pub_date',)


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
