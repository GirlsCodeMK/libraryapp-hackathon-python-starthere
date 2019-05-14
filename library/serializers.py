from django.contrib.auth.models import User, Group
from rest_framework import serializers

from library.models import Book, Copy, Loan, UserMicrobit

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')

class UserMicrobitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserMicrobit
        fields = ('url', 'id', 'microbit_id', 'last_microbit_update',)

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = ('url', 'loaned_copy', 'borrower', 
            'loan_start', 'return_due', 'date_returned')

class CopySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Copy
        fields = ('url', 'book', 'copy_number', 'condition', 'acquisition_date',
            'available', 'on_loan',
            'microbit_id', 'last_microbit_update')

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'title', 'author', 'isbn', 'copy_available', 'publication_date', 'copies')
