from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-loans'),
    path('loans/', views.LoanedBooksAllListView.as_view(), name='all-loans'),
    path('loan/<uuid:pk>/renew/', views.renew_loan_librarian, name='renew-loan-librarian'),
]