from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author, verbose_name='book authors')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name='book publisher')
    pubdate = models.DateField('publication date')

    def __str__(self):
        return self.name

    def display_authors(self):
        """Creates a string for the Author. This is required to display author in Admin."""
        return ', '.join([authors.name for authors in self.authors.all()[:3]])

    display_authors.short_description = 'Authors'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book, verbose_name='store books')

    def __str__(self):
        return self.name

    def display_books(self):
        """Creates a string for the Book. This is required to display book in Admin."""
        return ', '.join([books.name for books in self.books.all()[:3]])

    display_books.short_description = 'Books'
