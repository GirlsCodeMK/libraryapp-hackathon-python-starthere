from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_loans'),
    path('copy/create/', views.CopyCreate.as_view(), name='copy_create'),
    path('copy/<int:pk>/update/', views.CopyUpdate.as_view(), name='copy_update'),
    path('copy/<int:pk>/delete/', views.CopyDelete.as_view(), name='copy_delete'),
    path('loans/', views.LoanedBooksAllListView.as_view(), name='all_loans'),
    path('loans-open-closed/', views.LoanedBooksAllOpenClosedListView.as_view(), name='all_open_closed_loans'),
    path('loan/<uuid:pk>/return/', views.return_loan_librarian, name='return_loan_librarian'),
    path('loan/<uuid:pk>/renew/', views.renew_loan_librarian, name='renew_loan_librarian'),
    path('loan/create/', views.LoanCreate.as_view(), name='loan_create'),
    path('loan/<uuid:pk>/update/', views.LoanUpdate.as_view(), name='loan_update'),
    path('loan/<uuid:pk>/delete/', views.LoanDelete.as_view(), name='loan_delete'),
    path('issue/', views.issue_find_user, name='issue_find_user'),
    path('issue-to/<int:user_pk>', views.issue_to_user, name='issue_to_user'),
]
