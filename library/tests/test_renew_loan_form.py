from django.test import TestCase, override_settings
from django.utils import timezone
from django.urls import reverse

from library.forms import RenewLoanForm
from library.models import Book, Copy, Loan
from django.contrib.auth.models import User, Group

import datetime
import uuid

# Test the form itself
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')
class RenewLoanFormTest(TestCase):

    fixtures = ['config',]

    def test_renew_form_date_field_label(self):
        form = RenewLoanForm()
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewLoanForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewLoanForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewLoanForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewLoanForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = RenewLoanForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())


# Test the view underlying the form
@override_settings(STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage')
class RenewLoanLibrarianViewTest(TestCase):

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
        
        test_book = Book.objects.create(
            title='Test title',
            author='Test author',
            edition=1,
            isbn='1234',
            publication_date=datetime.date.today() - datetime.timedelta(weeks=50),
        )

        # Create 2 Copy objects and a Loan for each. 
        # Note that the Loans are attributes of this object
        test_copy1 = Copy.objects.create(
            book = test_book,
            acquisition_date = datetime.date.today() - datetime.timedelta(weeks=1),
            copy_number = 1,
            condition = 'M',
            )
        self.test_loan1 = Loan.objects.create(
            loaned_copy = test_copy1,
            borrower = test_user,
            loan_start = datetime.date.today() - datetime.timedelta(days=1),
            return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
            )

        test_copy2 = Copy.objects.create(
            book = test_book,
            acquisition_date = datetime.date.today() - datetime.timedelta(weeks=2),
            copy_number = 2,
            condition = 'M',
            )
        self.test_loan2 = Loan.objects.create(
            loaned_copy = test_copy2,
            borrower = test_librarian,
            loan_start = datetime.date.today() - datetime.timedelta(days=1),
            return_due = datetime.date.today() - datetime.timedelta(days=1) + datetime.timedelta(weeks=3),
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk': self.test_loan1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser', password='F7NcNDVS')
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk': self.test_loan1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testlibrarian', password='ubE3AkC2')
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk': self.test_loan2.pk}))
        
        # Check that it lets us login - this is our book and we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testlibrarian', password='ubE3AkC2')
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk': self.test_loan1.pk}))
        
        # Check that it lets us login. We're a librarian, so we can view any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        login = self.client.login(username='testlibrarian', password='ubE3AkC2')
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk':test_uid}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testlibrarian', password='ubE3AkC2')
        response = self.client.get(reverse('renew_loan_librarian', kwargs={'pk': self.test_loan1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'library/loan_renew_librarian.html')
