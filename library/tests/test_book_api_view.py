from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from django.contrib.auth.models import User, Group

from library.models import Book
from library.views import BookViewSet
import datetime
import json

# Override the compiled static file storage for testing, 
# so the test harness can find things like the style sheets
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')
class BookListAllViewTest(TestCase):

    fixtures = ['config',]

    @classmethod
    def setUpTestData(cls):
        # Create 13 books for pagination tests
        number_of_books = 13

        for book_id in range(10, number_of_books + 10):
            Book.objects.create(
                title=f'Title {book_id}',
                author=f'Person {book_id}',
                edition=book_id,
                isbn='1234',
                publication_date=datetime.date.today(),
            )
           
    def test_view_url_exists_at_desired_location(self):
        factory = APIRequestFactory()
        request = factory.get('/library/api/v1/books')
        view = BookViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_ten(self):
        factory = APIRequestFactory()
        view = BookViewSet.as_view({'get': 'list'})
        request = factory.get('/library/api/v1/books')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        response_json = json.loads(response.content)
        self.assertTrue(response_json['count'] == 13)
        self.assertIsNone(response_json['previous'])
        self.assertIsNotNone(response_json['next'])
        self.assertTrue(len(response_json['results']) == 10)

    def test_lists_all_books(self):
        factory = APIRequestFactory()
        view = BookViewSet.as_view({'get': 'list'})
        request = factory.get('/library/api/v1/books')
        response = view(request)
        response.render()
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        second_page = response_json['next']
        
        request = factory.get(second_page)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        response_json = json.loads(response.content)
        self.assertTrue(response_json['count'] == 13)
        self.assertIsNotNone(response_json['previous'])
        self.assertIsNone(response_json['next'])
        self.assertTrue(len(response_json['results']) == 3)

# Test the view underlying the form
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')
class BookViewCreationTest(TestCase):

    fixtures = ['config',]

    def setUp(self):
        # Create users
        test_user = User.objects.create_user(username='testuser', password='F7NcNDVS')
        test_librarian = User.objects.create_user(username='testlibrarian', password='ubE3AkC2')
        
        test_user.save()
        test_librarian.save()

        library_user_group = Group.objects.get(name='Library user')
        librarian_group = Group.objects.get(name='Librarian')
        test_user.groups.add(library_user_group)
        test_librarian.groups.add(library_user_group, librarian_group)
        
        self.test_book = Book.objects.create(
            title='Test title',
            author='Test author',
            edition=1,
            isbn='1234',
            publication_date=datetime.date.today() - datetime.timedelta(weeks=50),
        )

        # # Create 2 Copy objects and a Loan for each. 
        # # Note that the Loans are attributes of this object
        # test_copy1 = Copy.objects.create(
        #     book = test_book,
        #     acquisition_date = datetime.date.today() - datetime.timedelta(weeks=1),
        #     copy_number = 1,
        #     condition = 'M',
        #     )
        # self.test_loan1 = Loan.objects.create(
        #     loaned_copy = test_copy1,
        #     borrower = test_user,
        #     loan_start = datetime.date.today() - datetime.timedelta(days=1),
        #     return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
        #     )

        # test_copy2 = Copy.objects.create(
        #     book = test_book,
        #     acquisition_date = datetime.date.today() - datetime.timedelta(weeks=2),
        #     copy_number = 2,
        #     condition = 'M',
        #     )
        # self.test_loan2 = Loan.objects.create(
        #     loaned_copy = test_copy2,
        #     borrower = test_librarian,
        #     loan_start = datetime.date.today() - datetime.timedelta(days=1),
        #     return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
        #     )

    def test_user_can_view_book(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testuser')
        request = factory.get('/library/api/v1/books')
        view = BookViewSet.as_view({'get': 'retrieve'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_book.pk)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_edit_book(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testuser')
        request = factory.patch('/library/api/v1/books/', {'title': 'New title'})
        view = BookViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_book.pk)
        self.assertEqual(response.status_code, 403)

    def test_librarian_can_view_book(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testlibrarian')
        request = factory.get('/library/api/v1/books')
        view = BookViewSet.as_view({'get': 'retrieve'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_book.pk)
        self.assertEqual(response.status_code, 200)

    def test_librarian_can_edit_book(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testlibrarian')
        request = factory.patch('/library/api/v1/books/', {'title': 'New title'})
        view = BookViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_book.pk)
        self.assertEqual(response.status_code, 200)
