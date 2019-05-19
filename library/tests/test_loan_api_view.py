from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from django.contrib.auth.models import User, Group

from library.models import Book, Copy, Loan
from library.views import LoanViewSet
import datetime
import json

# Override the compiled static file storage for testing, 
# so the test harness can find things like the style sheets
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')

class LoanViewUpdateTest(TestCase):

    fixtures = ['config',]

    def setUp(self):
        # Create users
        test_user = User.objects.create_user(username='testuser', password='F7NcNDVS')
        test_assistant = User.objects.create_user(username='testassistant', password='ubE3AkCa')
        test_librarian = User.objects.create_user(username='testlibrarian', password='ubE3AkC2')
        
        test_user.save()
        test_assistant.save()
        test_librarian.save()

        library_user_group = Group.objects.get(name='Library user')
        library_assistant_group = Group.objects.get(name='Library assistant')
        librarian_group = Group.objects.get(name='Librarian')
        test_user.groups.add(library_user_group)
        test_assistant.groups.add(library_user_group)
        test_assistant.groups.add(library_assistant_group)
        test_librarian.groups.add(library_user_group, librarian_group)
        
        test_book = Book.objects.create(
            title='Test title',
            author='Test author',
            edition=1,
            isbn='1234',
            publication_date=datetime.date.today() - datetime.timedelta(weeks=50),
        )

        # Create 2 Copy objects and a Loan for each. 
        # Note that the Loans are attributes of this object
        self.test_copy1 = Copy.objects.create(
            book = test_book,
            acquisition_date = datetime.date.today() - datetime.timedelta(weeks=1),
            copy_number = 1,
            condition = 'M',
            )
        self.test_loan1 = Loan.objects.create(
            loaned_copy = self.test_copy1,
            borrower = test_user,
            loan_start = datetime.date.today() - datetime.timedelta(days=1),
            return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
            )

        self.test_copy2 = Copy.objects.create(
            book = test_book,
            acquisition_date = datetime.date.today() - datetime.timedelta(weeks=2),
            copy_number = 2,
            condition = 'M',
            )
        self.test_loan2 = Loan.objects.create(
            loaned_copy = self.test_copy2,
            borrower = test_librarian,
            loan_start = datetime.date.today() - datetime.timedelta(days=1),
            return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
            )

    def test_user_cannot_view_loan(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testuser')
        request = factory.get('/library/api/v1/loans/{}'.format(self.test_loan2.id))
        view = LoanViewSet.as_view({'get': 'retrieve'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_loan2.id)
        self.assertEqual(response.status_code, 200)

    def test_librarian_can_renew_loan(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testlibrarian')
        request = factory.patch(
            '/library/api/v1/loans/{}'.format(self.test_loan2.id), 
            {'return_due': '2019-02-01'})
        view = LoanViewSet.as_view({'patch': 'partial_update'})
        force_authenticate(request, user=user)
        response = view(request, pk=self.test_loan2.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['return_due'], '2019-02-01')

    def test_assistant_can_create_loan(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='testuser')
        assistant = User.objects.get(username='testassistant')
        request = factory.post(
            '/library/api/v1/loans/', 
            {'loaned_copy': '/library/api/v1/copies/{}/'.format(self.test_copy1.id),
             'borrower': '/library/api/v1/users/{}/'.format(user.id),
             'loan_start': '2019-01-01',
             'return_due': '2019-02-01',
             })
        view = LoanViewSet.as_view({'post': 'create'})
        force_authenticate(request, user=assistant)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['return_due'], '2019-02-01')
