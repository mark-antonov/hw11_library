import random

from bookstore.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand
from django.utils import timezone

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'This command is for inserting Author, Book, Publisher, Store into database.' \
           'Insert 10, Authors, 10 Publishers, 200 Books, 10 Stores.'  # noqa: A003

    def handle(self, *args, **kwargs):
        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()

        # create 10 authors
        authors = [Author(name=fake.name(), age=random.randint(18, 85)) for _ in range(10)]
        Author.objects.bulk_create(authors)

        # create 10 publishers
        publishers = [Publisher(name=fake.company()) for _ in range(10)]
        Publisher.objects.bulk_create(publishers)

        # create 20 books for every publishers
        for publisher in Publisher.objects.all():
            for _ in range(20):
                books = [Book(name=fake.sentence(nb_words=3), pages=random.randint(25, 300),
                              price=round(random.uniform(15, 300), 1), rating=random.randint(1, 10),
                              pubdate=timezone.now(), publisher=publisher)]
                Book.objects.bulk_create(books)

        # create 10 stores and insert 20 books in every store
        books = list(Book.objects.all())
        for _ in range(10):
            temp_books = [books.pop(0) for _ in range(20)]
            store = Store.objects.create(name=fake.company())
            store.books.set(temp_books)
            store.save()

        # получаем списки id книг и авторов
        book_ids = list(Book.objects.values_list('id', flat=True))
        author_ids = list(Author.objects.values_list('id', flat=True))

        # для каждой книги
        for book_id in book_ids:
            # создаем список авторов
            authors_of_book = []
            # перетасовываем авторов
            random.shuffle(author_ids)

            # получаем список id случайного числа авторов
            book_authors = author_ids[:random.randint(1, len(author_ids))]

            # для каждого автора в списке
            for author_id in book_authors:
                # создаем связь автора с книгой
                book_author = Book.authors.through(book_id=book_id, author_id=author_id)
                # добавляем эту связь в список
                authors_of_book.append(book_author)

            # добавляем книге связи со всеми ее авторами
            Book.authors.through.objects.bulk_create(authors_of_book)

        self.stdout.write(self.style.SUCCESS('Successfully!'))
