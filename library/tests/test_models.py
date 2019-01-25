from django.test import TestCase

# Create your tests here.

from library.models import Book, Copy, Loan
from django.contrib.auth.models import User
from datetime import date

class BookModelTest(TestCase):

    fixtures = ['config', 'small_test_data.json',]

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=1)
        expected_object_name = book.title
        self.assertEquals(expected_object_name, str(book))

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(book.get_absolute_url(), '/library/book/1')

class CopyModelTest(TestCase):

    fixtures = ['config', 'small_test_data.json',]
    
    def test_object_name_is_title_and_copy_number(self):
        copy = Copy.objects.get(id=1)
        expected_object_name = '{} ({})'.format(copy.book.title, copy.copy_number)
        self.assertEquals(expected_object_name, str(copy))

    def test_get_absolute_url(self):
        copy = Copy.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(copy.get_absolute_url(), '/library/book/1')

    def test_on_loan_property(self):
        copy1 = Copy.objects.get(id=1) # an open loan
        self.assertTrue(copy1.on_loan)
        self.assertFalse(copy1.available)

        copy3 = Copy.objects.get(id=3) # no open loans
        self.assertFalse(copy3.on_loan)
        self.assertTrue(copy3.available)

        copy5 = Copy.objects.get(id=5) # Destroyed, no loans
        self.assertFalse(copy5.on_loan)
        self.assertFalse(copy5.available)

class LoanModelTest(TestCase):

    fixtures = ['config', 'small_test_data.json',]

    def test_object_name_is_title_and_copy_number(self):
        loan1 = Loan.objects.get(id="0ec31922-fc6b-417c-b665-af05d55ba77c")
        expected_object_name = '{} ; {} : {} -> open'.format(loan1.loaned_copy, loan1.borrower, loan1.loan_start)
        self.assertEquals(expected_object_name, str(loan1))

        loan2 = Loan.objects.get(id="8959a803-02b9-4afa-bee1-17b3a7fe5685")
        expected_object_name = '{} ; {} : {} -> {}'.format(loan2.loaned_copy, loan2.borrower, loan2.loan_start, loan2.date_returned)
        self.assertEquals(expected_object_name, str(loan2))
    
    def test_get_absolute_url(self):
        loan = Loan.objects.get(id="0ec31922-fc6b-417c-b665-af05d55ba77c")
        # This will also fail if the urlconf is not defined.
        self.assertEquals(loan.get_absolute_url(), '/library/book/1')
    
