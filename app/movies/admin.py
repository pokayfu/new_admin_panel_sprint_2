from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created',)
    search_fields = ('full_name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created',)
    list_filter = ('name',)
    search_fields = ('description', 'id')
