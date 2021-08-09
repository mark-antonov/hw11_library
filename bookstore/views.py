from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count, Max, Min
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ContactForm
from .models import Author, Book, Publisher, Store
from .tasks import contact_us_send_mail


# def index(request):
#     num_books = Book.objects.count()
#     num_authors = Author.objects.count()
#     num_publishers = Publisher.objects.count()
#     num_stores = Store.objects.count()
#     context = {
#         'num_books': num_books,
#         'num_authors': num_authors,
#         'num_publishers': num_publishers,
#         'num_stores': num_stores
#     }
#     return render(request, 'index.html', context)


@cache_page(10)
def authors(request):
    # authors = Author.objects.all()
    authors = Author.objects.prefetch_related('book_set__authors')
    avg_age = Author.objects.all().aggregate(avg_age=Avg('age'))
    avg_rating = Author.objects.aggregate(avg_rating=Avg('book__rating'))
    context = {
        'authors': authors,
        'avg_age': round(avg_age['avg_age']),
        'avg_rating': round(avg_rating['avg_rating'], 2)
    }
    return render(request, 'authors.html', context)


@cache_page(10)
def authors_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.select_related('publisher')
    return render(request, 'authors_detail.html', {'author': author, 'books': books})


@cache_page(10)
def publishers(request):
    publishers = Publisher.objects.all().annotate(num_books=Count('book'))
    return render(request, 'publishers.html', {'publishers': publishers})


@cache_page(10)
def publishers_detail(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk)
    books = Book.objects.prefetch_related('authors')
    return render(request, 'publishers_detail.html', {'publisher': publisher, 'books': books})


# def books(request):
#     # books = Book.objects.annotate(num_rating=Max('rating')).order_by('-num_rating')  # по рейтингу
#     books = Book.objects.annotate(num_authors=Count('authors')).select_related('publisher')
#     avg_price = Book.objects.all().aggregate(avg_price=Avg('price'))
#     max_price = Book.objects.all().aggregate(max_price=Max('price'))
#     min_price = Book.objects.all().aggregate(min_price=Min('price'))
#     context = {
#         'books': books,
#         'avg_price': round(avg_price['avg_price'], 2),
#         'max_price': round(max_price['max_price'], 2),
#         'min_price': round(min_price['min_price'], 2)
#     }
#     return render(request, 'books.html', context)


# def books_detail(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'books_detail.html', {'book': book})

@cache_page(10)
def stores(request):
    stores = Store.objects.all().annotate(num_books=Count('books'))
    return render(request, 'stores.html', {'stores': stores})


@cache_page(10)
def stores_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    books = Book.objects.prefetch_related('authors')
    return render(request, 'stores_detail.html', {'store': store, 'books': books})


# HT 14. Class based views, pagination
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        context['num_authors'] = Author.objects.count()
        context['num_publishers'] = Publisher.objects.count()
        context['num_stores'] = Store.objects.count()
        return context


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'book_create.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_url = reverse_lazy('books')
    login_url = '/admin/login/'


class BookUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'book_update.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_message = "Book successfully updated!"
    login_url = '/admin/login/'
    redirect_field_name = 'admin'

    def get_success_url(self):
        book_id = self.kwargs['pk']
        return reverse_lazy('book-update', kwargs={'pk': book_id})


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book_delete.html'
    success_url = reverse_lazy('books')
    login_url = '/admin/login/'


@method_decorator(cache_page(10), name='dispatch')
class BookDetail(DetailView):
    model = Book
    template_name = 'books_detail.html'


@method_decorator(cache_page(10), name='dispatch')  # HT 15. Django redis cache
class BookList(ListView):
    model = Book
    template_name = 'books.html'
    paginate_by = 100
    queryset = Book.objects.annotate(num_authors=Count('authors')).select_related('publisher')
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg'] = Book.objects.all().aggregate(avg_price=Avg('price'), max_price=Max('price'),
                                                      min_price=Min('price'))
        return context


# HT 19. Bootstrap, JQuery, JSON, AJAX
def contact_form(request):
    data = dict()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            data['form_is_valid'] = True
            contact_us_send_mail.delay(subject, message, from_email, ['admin@example.com'])
            messages.add_message(request, messages.SUCCESS, 'Message sent')
        else:
            data['form_is_valid'] = False
    else:
        form = ContactForm()
    context = {'form': form}
    data['html_form'] = render_to_string(template_name='contact.html', context=context, request=request)
    return JsonResponse(data)
