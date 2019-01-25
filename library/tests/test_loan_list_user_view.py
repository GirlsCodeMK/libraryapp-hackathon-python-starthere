from django.test import TestCase, override_settings
from django.urls import reverse

from library.models import Book, Copy, Loan
from django.contrib.auth.models import User, Group

import datetime

# Override the compiled static file storage for testing, 
# so the test harness can find things like the style sheets
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')
class LoanListByUserViewTest(TestCase):

    fixtures = ['config',]
    
    @classmethod
    def setUp(cls):
        test_user1 = User.objects.create_user(username='testuser1', password='F7NcNDVS')
        test_user2 = User.objects.create_user(username='testuser2', password='ubE3AkC2')
        
        test_user1.save()
        test_user2.save()

        library_user_group = Group.objects.get(name='Library user')
        test_user1.groups.add(library_user_group)
        test_user2.groups.add(library_user_group)
        
        test_book = Book.objects.create(
            title='Test title',
            author='Test author',
            edition=1,
            isbn='1234',
            publication_date=datetime.date.today() - datetime.timedelta(weeks=50),
        )

        # Create 10 Copy objects
        number_of_copies = 10
        for copy_number in range(number_of_copies):
            copy = Copy.objects.create(
                book = test_book,
                acquisition_date = datetime.date.today() - datetime.timedelta(weeks=(copy_number % 3)),
                copy_number = copy_number,
                condition = 'M',
                )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_loans'))
        self.assertRedirects(response, '/accounts/login/?next=/library/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='F7NcNDVS')
        response = self.client.get(reverse('my_loans'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/loan_list_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='F7NcNDVS')
        response = self.client.get(reverse('my_loans'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        
        # Check that initially we don't have any books in list (none on loan)
        self.assertTrue('loan_list' in response.context)
        self.assertEqual(len(response.context['loan_list']), 0)
        
        # Now change all copies to be on loan
        test_user1 = User.objects.get(username='testuser1')
        test_user2 = User.objects.get(username='testuser2')
        for copy_number, copy in enumerate(Copy.objects.all()):
            the_borrower = test_user1 if copy_number % 2 else test_user2
            the_loan_start = datetime.date.today() - datetime.timedelta(days=(copy_number % 3))
            Loan.objects.create(    
                loaned_copy = copy,
                borrower = the_borrower,
                loan_start = the_loan_start,
                return_due = the_loan_start + datetime.timedelta(weeks=3),
                )

        # Check that now we have borrowed books in the list
        response = self.client.get(reverse('my_loans'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue('loan_list' in response.context)
        
        # Confirm all books belong to testuser1 and are on loan
        for loan in response.context['loan_list']:
            self.assertEqual(response.context['user'], loan.borrower)
            self.assertTrue(loan.date_returned is None)

    def test_pages_ordered_by_due_date(self):
        # Now change all copies to be on loan
        test_user1 = User.objects.get(username='testuser1')
        test_user2 = User.objects.get(username='testuser2')
        for copy_number, copy in enumerate(Copy.objects.all()):
            the_borrower = test_user1 if copy_number % 2 else test_user2
            the_loan_start = datetime.date.today() - datetime.timedelta(days=(copy_number % 3))
            Loan.objects.create(    
                loaned_copy = copy,
                borrower = the_borrower,
                loan_start = the_loan_start,
                return_due = the_loan_start + datetime.timedelta(weeks=3),
                )

        login = self.client.login(username='testuser1', password='F7NcNDVS')
        response = self.client.get(reverse('my_loans'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
                
        # Confirm that of the items, only 10 are displayed due to pagination.
        self.assertEqual(len(response.context['loan_list']), 5)
        
        last_date = 0
        for loan in response.context['loan_list']:
            if last_date == 0:
                last_date = loan.return_due
            else:
                self.assertTrue(last_date <= loan.return_due)
                last_date = loan.return_due
 