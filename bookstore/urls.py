from django.urls import path
from django.views.decorators.cache import cache_page  # HT 15. Django redis cache

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.HomePageView.as_view(), name='index'),

    path('authors/', views.authors, name='authors'),
    path('authors/<int:pk>/', views.authors_detail, name='authors_detail'),

    path('publishers/', views.publishers, name='publishers'),
    path('publishers/<int:pk>/', views.publishers_detail, name='publishers_detail'),

    # path('books/', views.books, name='books'),
    # path('books/<int:pk>/', views.books_detail, name='books_detail'),

    path('stores/', views.stores, name='stores'),
    path('stores/<int:pk>/', views.stores_detail, name='stores_detail'),

    # HT 14. Class based views, pagination
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/update/<int:pk>/', views.BookUpdate.as_view(), name='book-update'),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>/', cache_page(10)(views.BookDetail.as_view()), name='books_detail'),
    path('books/', views.BookList.as_view(), name='books'),
]
