from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:pk>/', views.authors_detail, name='authors_detail'),
    path('publishers/', views.publishers, name='publishers'),
    path('publishers/<int:pk>/', views.publishers_detail, name='publishers_detail'),
    path('books/', views.books, name='books'),
    path('books/<int:pk>/', views.books_detail, name='books_detail'),
    path('stores/', views.stores, name='stores'),
    path('stores/<int:pk>/', views.stores_detail, name='stores_detail'),
]
