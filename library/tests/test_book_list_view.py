from django.test import TestCase, override_settings
from django.urls import reverse

from library.models import Book
import datetime

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
        response = self.client.get('/library/books/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/book_list.html')
        
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['book_list'].has_previous() == False)
        self.assertTrue(response.context['book_list'].has_next() == True)
        self.assertTrue(len(response.context['book_list']) == 10)

    def test_lists_all_books(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('book_list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['book_list'].has_previous() == True)
        self.assertTrue(response.context['book_list'].has_next() == False)
        self.assertTrue(len(response.context['book_list']) == 3)
