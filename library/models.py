from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid # Required for unique loan instances

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    edition = models.PositiveIntegerField()
    isbn = models.CharField(max_length=17)
    publication_date = models.DateField()
    image = models.CharField(max_length=500,null=True, blank=True)
    thumbnail = models.CharField(max_length=500,null=True, blank=True)

    class Meta:
        ordering = ['title', 'edition', '-publication_date']

    def __str__(self):
        """String for representing the Book object (in Admin site etc.)."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_detail', args=[str(self.id)])

    @property
    def copy_available(self):
        """True if at least one copy of this book is available for loan, false otherwise"""
        # available_copy = False
        # for copy in self.copy_set.all():
        #     if copy.available:
        #         available_copy = True
        # return available_copy

        return any(copy for copy in self.copy_set.all() if copy.available)



class Copy(models.Model):
    COPY_CONDITIONS = (
        ('M', 'Mint'),
        ('G', 'Good'),
        ('W', 'Worn'),
        ('D', 'Damaged'),
        ('L', 'Lost'),
        ('X', 'Destroyed'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    acquisition_date = models.DateField()
    copy_number = models.PositiveIntegerField()
    condition = models.CharField(max_length=1, choices=COPY_CONDITIONS)

    class Meta:
        ordering = ['copy_number']
        verbose_name_plural = "copies"

    def __str__(self):
        """String for representing the Copy object."""
        return self.book.title + ' (' + str(self.copy_number) + ')'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_detail', args=[str(self.book.id)])

    @property
    def on_loan(self):
        return Loan.objects.filter(loaned_copy=self.id).filter(date_returned__isnull=True).count() > 0

    @property
    def available(self):
        return not(self.on_loan) and (self.condition not in ['L', 'X'])


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this loan across whole library")
    loaned_copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    loan_start = models.DateField()
    return_due = models.DateField()
    date_returned = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_returned', '-return_due', '-loan_start']
        permissions = (
            ("can_mark_loaned", "Set book as on loan"),
            ("can_mark_returned", "Set book as returned"),
            ("can_view_all_loans", "View all users' loans")
            )

    def __str__(self):
        """String for representing the Loan object."""
        base = '{} ; {} : {} -> '.format(self.loaned_copy, self.borrower, self.loan_start)
        if self.date_returned:
            return base + str(self.date_returned)
        return base + 'open'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_detail', args=[str(self.loaned_copy.book.id)])

    @property
    def is_overdue(self):
        if (not self.date_returned) and date.today() > self.return_due:
            return True
        return False

class Configuration(models.Model):
    maxbooksonloan = models.PositiveIntegerField()
