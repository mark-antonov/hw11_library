from django.contrib import admin

from .models import Author, Book, Publisher, Store


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "age"]
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "display_authors", "pages", "price", "rating", "publisher", "pubdate"]
    fields = ["name", "pages", "price", "rating", "authors", ("publisher", "pubdate")]
    date_hierarchy = "pubdate"  # date filter widget
    search_fields = ["name"]
    list_filter = ["rating", "authors", "publisher"]
    filter_horizontal = ["authors"]  # many-to-many relationship widget


class BookInline(admin.TabularInline):
    model = Book


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [BookInline]  # allows you to edit related objects on the same page as the parent object.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", 'display_books']
    filter_horizontal = ["books"]  # many-to-many relationship widget
